from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from datetime import datetime, date
from collections import defaultdict

from .models import Parada, ZonaPerfilVelocidad, HorarioDia
from trazabilidad.models import Flejes, Acumulador
from .dashboard_utils import _clamp, _segundos, _siglas_zona, _clave_agrupacion
import datetime as dt

# ─── cálculo OEE ─────────────────────────────────────────────────────────────

def _calcular_disponibilidad_rendimiento(periodos_planos, t_total_seg):
    t_prod      = 0.0
    t_run       = 0.0
    t_cambio    = 0.0
    rend_run    = 0.0
    rend_cambio = 0.0

    for p in periodos_planos:
        tipo = p['tipo_parada']
        seg  = p['seg']

        if tipo == 'Automatico':
            t_run    += seg
            rend_run += p['rendimiento'] * seg
        elif tipo == 'Cambio':
            t_cambio    += seg
            rend_cambio += p['rendimiento'] * seg

        if tipo in ('Automatico', 'Cambio'):
            t_prod += seg

    disponibilidad = (t_prod / t_total_seg) if t_total_seg > 0 else 0.0

    # Automatico: media ponderada directa
    if rend_run == 0:
        r_run = 1.0
    else:
        r_run = (rend_run / t_run) if t_run > 0 else 1.0

    # Cambio: si no hay rendimiento acumulado, asume 100% (igual que el frontend)
    if t_cambio > 0:
        r_cambio = (rend_cambio / t_cambio) if rend_cambio > 0 else 1.0
    else:
        r_cambio = 0.0

    if (t_run + t_cambio) > 0:
        rendimiento = (r_run * t_run + r_cambio * t_cambio) / (t_run + t_cambio)
    else:
        rendimiento = 0.0

    return {
        'disponibilidad': round(disponibilidad * 100, 2),
        'rendimiento':    round(rendimiento    * 100, 2),
        't_total_min':    round(t_total_seg / 60, 1),
        't_prod_min':     round(t_prod      / 60, 1),
    }


def _calcular_calidad(flejes):
    calidad    = 0.0
    peso_total = 0.0
    for f in flejes:
        metros_medido = f.metros_medido or 0
        peso          = f.peso or 0
        metros_tubo   = f.metros_tubo()
        if metros_medido > 0:
            calidad += metros_tubo * peso / metros_medido
        peso_total += peso
    if peso_total > 0:
        return round(calidad * 100 / peso_total, 2)
    return 100.0


def _oee(disp, rend, cal):
    return round((disp / 100) * (rend / 100) * (cal / 100) * 100, 2)


def _indicadores_completos(periodos_planos, t_total_seg, calidad):
    dr  = _calcular_disponibilidad_rendimiento(periodos_planos, t_total_seg)
    oee = _oee(dr['disponibilidad'], dr['rendimiento'], calidad)
    return {**dr, 'calidad': calidad, 'oee': oee}


# ─── horarios / turnos ───────────────────────────────────────────────────────

def _cargar_horarios(zona_id, fecha_min, fecha_max):
    desde = fecha_min - dt.timedelta(days=1)
    hasta = fecha_max + dt.timedelta(days=1)
    return {
        h.fecha: h
        for h in HorarioDia.objects.filter(zona_id=zona_id, fecha__range=(desde, hasta))
    }


def _construir_intervalos_turno(horarios):
    intervalos = defaultdict(list)

    for fecha, horario in horarios.items():
        inicio_dia = timezone.make_aware(datetime.combine(fecha, horario.inicio))
        fin_dia    = timezone.make_aware(datetime.combine(fecha, horario.fin))
        cambio1    = timezone.make_aware(datetime.combine(fecha, horario.cambio_turno_1))

        if horario.turno_mañana:
            intervalos[horario.turno_mañana.turno].append((inicio_dia, cambio1))

        if horario.turno_tarde:
            fin_tarde = fin_dia
            if horario.cambio_turno_2:
                fin_tarde = timezone.make_aware(datetime.combine(fecha, horario.cambio_turno_2))
            intervalos[horario.turno_tarde.turno].append((cambio1, fin_tarde))

        if horario.turno_noche and horario.cambio_turno_2:
            inicio_noche = timezone.make_aware(datetime.combine(fecha, horario.cambio_turno_2))

            # Fin real del turno de noche: el 'inicio' del HorarioDia del día siguiente, para poder cruzar medianoche correctamente.
            siguiente = horarios.get(fecha + dt.timedelta(days=1))
            if siguiente:
                fin_noche = timezone.make_aware(datetime.combine(siguiente.fecha, siguiente.inicio))
            else:
                # Sin dato del día siguiente: nos quedamos con el 'fin' de hoy (comportamiento anterior, mejor que fallar).
                fin_noche = fin_dia

            intervalos[horario.turno_noche.turno].append((inicio_noche, fin_noche))

    return intervalos


def _en_intervalo_turno(timestamp, letra_turno, intervalos_turno):
    for inicio, fin in intervalos_turno.get(letra_turno, []):
        if inicio <= timestamp <= fin:
            return True
    return False


def _flejes_del_turno(flejes_lista, letra_turno, intervalos_turno):
    resultado = []
    for f in flejes_lista:
        if not f.fecha_entrada or not f.hora_entrada:
            continue

        entrada = timezone.make_aware(datetime.combine(f.fecha_entrada, f.hora_entrada))
        entrada_dentro = _en_intervalo_turno(entrada, letra_turno, intervalos_turno)

        salida_dentro = False
        if f.fecha_salida and f.hora_salida:
            salida = timezone.make_aware(datetime.combine(f.fecha_salida, f.hora_salida))
            salida_dentro = _en_intervalo_turno(salida, letra_turno, intervalos_turno)

        if entrada_dentro or salida_dentro:
            resultado.append(f)

    return resultado


# ─── vista ───────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def oee_dashboard(request):
    zona_id     = request.GET.get('zona_id')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    agrupar     = request.GET.get('agrupar', 'dia')
    turnos_cfg  = request.GET.getlist('turnos') or ['A', 'B']

    if not all([zona_id, fecha_desde, fecha_hasta]):
        return Response({'error': 'zona_id, fecha_desde y fecha_hasta son obligatorios'}, status=400)

    try:
        f_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
        f_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': 'Formato de fecha inválido'}, status=400)

    dt_desde = timezone.make_aware(datetime.combine(f_desde, datetime.min.time()))
    dt_hasta = timezone.make_aware(datetime.combine(f_hasta, datetime.max.time()))

    siglas       = _siglas_zona(zona_id)
    perfil       = ZonaPerfilVelocidad.objects.get(zona_id=zona_id)

    horarios = _cargar_horarios(zona_id, f_desde, f_hasta)

    # ── 1. Paradas + periodos ─────────────────────────────────────────────────
    paradas_qs = (
        Parada.objects
        .filter(zona_id=zona_id)
        .filter(
            Q(periodos__inicio__gte=dt_desde, periodos__inicio__lte=dt_hasta) |
            Q(periodos__fin__gte=dt_desde,    periodos__fin__lte=dt_hasta)
        )
        .prefetch_related('periodos__turno', 'codigo__tipo')
        .distinct()
    )

    # ── 2. Flejes + tubos ─────────────────────────────────────────────────────────
    acc = Acumulador.objects.filter(maquina_siglas__iexact=siglas).last()

    if acc and acc.maquila_siglas:
        siglas_maquila = acc.maquila_siglas.upper()
        flejes_qs = (
            Flejes.objects
            .filter(
                Q(maquina_siglas__iexact=siglas) |
                Q(maquina_siglas__iexact=siglas_maquila)
            )
            .filter(
                Q(fecha_entrada__gte=f_desde, fecha_entrada__lte=f_hasta) |
                Q(fecha_salida__gte=f_desde,  fecha_salida__lte=f_hasta)  |
                Q(fecha_entrada__lte=f_hasta, fecha_salida__isnull=True)
            )
            .prefetch_related('tubos')
        )
    else:
        flejes_qs = (
            Flejes.objects
            .filter(maquina_siglas__iexact=siglas)
            .filter(
                Q(fecha_entrada__gte=f_desde, fecha_entrada__lte=f_hasta) |
                Q(fecha_salida__gte=f_desde,  fecha_salida__lte=f_hasta)  |
                Q(fecha_entrada__lte=f_hasta, fecha_salida__isnull=True)
            )
            .prefetch_related('tubos')
        )

    # ── 3. Distribuir periodos por clave y turno ──────────────────────────────
    grupos = defaultdict(lambda: defaultdict(list))

    for parada in paradas_qs:
        tipo = parada.codigo.tipo.nombre

        if tipo == 'TNP':
            continue
        try:
            rend_parada = parada.rendimiento() or 0
        except Exception:
            rend_parada = 0

        try:
            rend_por_turno = {
                rpt['turno']: (rpt['rendimiento'] or 0)
                for rpt in parada.rendimiento_por_turno()
            }
        except Exception:
            rend_por_turno = {}

        for periodo in parada.periodos.all():
            if not periodo.inicio:
                continue

            fin_real = periodo.fin if periodo.fin else timezone.now()
            p_ini    = _clamp(periodo.inicio, dt_desde, dt_hasta)
            p_fin    = _clamp(fin_real,       dt_desde, dt_hasta)

            if p_fin <= p_ini:
                continue

            turno_letra = periodo.turno.turno if periodo.turno else 'X'
            rend_turno = rend_por_turno.get(turno_letra, rend_parada)

            # CLAVE: dividir el periodo por días, y dentro de cada día,
            # recortar al horario laboral real de ESE día (no al día
            # completo 00:00-23:59). Así una parada o un tramo "Automático"
            # fuera de horario (de madrugada, en festivo, etc.) no infla el
            # t_total y no diluye disponibilidad/rendimiento.
            actual = p_ini

            while actual < p_fin:

                siguiente = min(
                    p_fin,
                    timezone.make_aware(datetime.combine(
                        actual.date() + dt.timedelta(days=1),
                        datetime.min.time()
                    ))
                )

                seg = _segundos(actual, siguiente)

                if seg > 0:
                    clave = _clave_agrupacion(actual.date(), agrupar)

                    periodo_plano = {
                        'tipo_parada': tipo,
                        'seg':         seg,
                        'rendimiento': rend_parada,
                    }

                    grupos[clave]['TOTAL'].append(periodo_plano)
                    grupos[clave][turno_letra].append(periodo_plano)

                actual = siguiente

    # ── 4. Flejes por clave ───────────────────────────────────────────────────
    flejes_por_clave = defaultdict(list)
    for f in flejes_qs:
        if not f.fecha_entrada:
            continue

        clave = _clave_agrupacion(f.fecha_entrada, agrupar)
        flejes_por_clave[clave].append(f)

    # Intervalos reales de cada turno (letra → lista de (inicio, fin)), a partir del mismo diccionario de horarios ya cargado.
    intervalos_turno = _construir_intervalos_turno(horarios)

    # ── 5. Construir respuesta ────────────────────────────────────────────────
    resultado = []

    for clave in sorted(grupos.keys()):

        periodos_total = grupos[clave]['TOTAL']
        t_total_seg    = sum(p['seg'] for p in periodos_total)
        todos_flejes   = flejes_por_clave.get(clave, [])
        calidad        = _calcular_calidad(todos_flejes)

        total = _indicadores_completos(periodos_total, t_total_seg, calidad)

        turnos_resultado = {}
        for t in turnos_cfg:
            periodos_turno = grupos[clave].get(t, [])
            t_turno_seg    = sum(p['seg'] for p in periodos_turno)

            if t_turno_seg == 0:
                turnos_resultado[t] = None
                continue

            # Clasificar flejes de esta clave según el turno, usando la línea
            # Válido para agrupar='dia', 'mes' y 'rango' por igual.
            flejes_turno = _flejes_del_turno(todos_flejes, t, intervalos_turno)
            calidad_turno = _calcular_calidad(flejes_turno) if flejes_turno else calidad

            turnos_resultado[t] = _indicadores_completos(
                periodos_turno, t_turno_seg, calidad_turno
            )

        resultado.append({
            'periodo': clave,
            'total':   total,
            'turnos':  turnos_resultado,
        })

    return Response(resultado)