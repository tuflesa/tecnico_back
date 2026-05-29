from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime, date
from collections import defaultdict

from velocidad.models import Parada, Periodo
from trazabilidad.models import Flejes
from estructura.models import Zona
from rest_framework.permissions import AllowAny
from velocidad.models import ZonaPerfilVelocidad


# ─── helpers ─────────────────────────────────────────────────────────────────

def _clamp(value, lo, hi):
    return max(lo, min(hi, value))


def _segundos(inicio, fin):
    return max(0.0, (fin - inicio).total_seconds())


def _siglas_zona(zona_id):
    return Zona.objects.get(id=zona_id).siglas.upper()


def _clave_agrupacion(fecha, agrupar):
    if isinstance(fecha, str):
        fecha = date.fromisoformat(fecha)
    return fecha.strftime('%Y-%m') if agrupar == 'mes' else fecha.strftime('%Y-%m-%d')


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
    r_run = (rend_run / t_run) if t_run > 0 else 0.0

    # Cambio: si no hay rendimiento acumulado, asume 100% (igual que el JS)
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
    """
    Replica exacta de calculaCalidad() del JS de tu compañero.
    Requiere que los flejes tengan prefetch de tubos.
    """
    calidad    = 0.0
    peso_total = 0.0

    for f in flejes:
        metros_medido = f.metros_medido or 0
        peso          = f.peso or 0
        metros_tubo   = f.metros_tubo()   # ya tiene prefetch, no hay N+1

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


# ─── vista ───────────────────────────────────────────────────────────────────

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def oee_dashboard(request):
    zona_id     = request.GET.get('zona_id')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    agrupar     = request.GET.get('agrupar', 'dia')   # 'dia' | 'mes'
    turnos_cfg  = request.GET.getlist('turnos') or ['A', 'B']

    if not all([zona_id, fecha_desde, fecha_hasta]):
        return Response(
            {'error': 'zona_id, fecha_desde y fecha_hasta son obligatorios'},
            status=400
        )

    try:
        f_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
        f_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': 'Formato de fecha inválido'}, status=400)

    dt_desde = timezone.make_aware(datetime.combine(f_desde, datetime.min.time()))
    dt_hasta = timezone.make_aware(datetime.combine(f_hasta, datetime.max.time()))

    siglas = _siglas_zona(zona_id)

    # ── 1. Paradas + periodos ────────────────────────────────────────────────
    # Solo las que tienen al menos un periodo dentro del rango
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

    # ── 2. Flejes + tubos (prefetch para evitar N+1 en metros_tubo()) ────────
    flejes_qs = (
        Flejes.objects
        .filter(maquina_siglas__iexact=siglas)
        .filter(
            Q(fecha_entrada__gte=f_desde, fecha_entrada__lte=f_hasta) |
            Q(fecha_salida__gte=f_desde,  fecha_salida__lte=f_hasta)  |
            Q(fecha_entrada__lte=f_hasta, fecha_salida__isnull=True)   # en proceso
        )
        .prefetch_related('tubos')   # ← clave para que metros_tubo() no haga N+1
    )

    # ── 3. Distribuir periodos por clave (día o mes) y turno ─────────────────
    # grupos[clave]['TOTAL'] = [periodos planos]
    # grupos[clave]['A']     = [periodos planos del turno A]
    grupos = defaultdict(lambda: defaultdict(list))

    for parada in paradas_qs:
        tipo = parada.codigo.tipo.nombre
        if tipo == 'TNP':
            continue

        perfil = ZonaPerfilVelocidad.objects.get(zona_id=zona_id)
        v_max_perfil = perfil.v_max

        # Replica exacta de Parada.rendimiento() con v_max del perfil
        if tipo == 'Automatico':
            t_p = 0.0
            r_p = 0.0
            for p in parada.periodos.all():
                fin_p = p.fin if p.fin else timezone.now()
                T = abs((fin_p - p.inicio).total_seconds()) / 60.0
                t_p += T
                if v_max_perfil > 0 and p.vmax > 0:  # ← igual que el modelo: solo si vmax > 0
                    r_p += (p.velocidad / v_max_perfil) * T
            rend_parada = (r_p / t_p) if t_p > 0 else 0.0
        else:
            rend_parada = 0.0  # Cambio siempre devuelve 0, igual que el modelo
        for periodo in parada.periodos.all():
            if not periodo.inicio:
                continue

            fin_real = periodo.fin if periodo.fin else timezone.now()

            p_ini = _clamp(periodo.inicio, dt_desde, dt_hasta)
            p_fin = _clamp(fin_real, dt_desde, dt_hasta)
            seg   = _segundos(p_ini, p_fin)
            if seg <= 0:
                continue

            turno_letra = periodo.turno.turno if periodo.turno else 'X'
            clave       = _clave_agrupacion(p_ini.date(), agrupar)

            periodo_plano = {
                'tipo_parada': tipo,
                'seg':         seg,
                'rendimiento':  rend_parada,
            }

            grupos[clave]['TOTAL'].append(periodo_plano)
            grupos[clave][turno_letra].append(periodo_plano)

    # ── 4. Distribuir flejes por clave ───────────────────────────────────────
    flejes_por_clave = defaultdict(list)
    for f in flejes_qs:
        if f.fecha_entrada:
            clave = _clave_agrupacion(f.fecha_entrada, agrupar)
            flejes_por_clave[clave].append(f)

    # ── 5. Construir respuesta ───────────────────────────────────────────────
    resultado = []

    for clave in sorted(grupos.keys()):
        periodos_total = grupos[clave]['TOTAL']
        t_total_seg    = sum(p['seg'] for p in periodos_total)
        calidad        = _calcular_calidad(flejes_por_clave.get(clave, []))

        total = _indicadores_completos(periodos_total, t_total_seg, calidad)

        turnos_resultado = {}
        for t in turnos_cfg:
            periodos_turno = grupos[clave].get(t, [])
            t_turno_seg    = sum(p['seg'] for p in periodos_turno)

            if t_turno_seg == 0:
                turnos_resultado[t] = None
                continue

            turnos_resultado[t] = _indicadores_completos(
                periodos_turno, t_turno_seg, calidad
            )

        resultado.append({
            'periodo':  clave,
            'total':    total,
            'turnos':   turnos_resultado,
        })

    debug = []
    for parada in paradas_qs:
        if parada.codigo.tipo.nombre == 'Automatico':
            periodos_p = list(parada.periodos.all())
            t_p = 0.0
            r_p = 0.0
            for p in periodos_p:
                if p.fin and p.inicio:
                    T = abs((p.fin - p.inicio).total_seconds()) / 60.0
                    t_p += T
                    r_p += ((p.velocidad or 0) / 80) * T
            rend = (r_p / t_p) if t_p > 0 else 0
            debug.append({
                'parada_id': parada.id,
                'codigo': parada.codigo.nombre,  # ← nombre del código de parada
                'tipo': parada.codigo.tipo.nombre,
                'inicio': str(periodos_p[0].inicio) if periodos_p else None,
                'n_periodos': len(periodos_p),
                't_min': round(t_p, 1),
                'rend': round(rend * 100, 1)
            })
        
    # DEBUG: muestra los primeros 5 periodos planos del TOTAL del primer día
    primera_clave = sorted(grupos.keys())[0]
    periodos_total = grupos[primera_clave]['TOTAL']

    t_auto = sum(p['seg'] for p in periodos_total if p['tipo_parada'] == 'Automatico')
    t_cambio = sum(p['seg'] for p in periodos_total if p['tipo_parada'] == 'Cambio')
    t_resto = sum(p['seg'] for p in periodos_total if p['tipo_parada'] not in ('Automatico', 'Cambio'))

    return Response({
        'resultado': resultado,
        'resumen_tiempos': {
            't_automatico_min': round(t_auto/60, 1),
            't_cambio_min': round(t_cambio/60, 1),
            't_resto_min': round(t_resto/60, 1),
            't_total_min': round((t_auto+t_cambio+t_resto)/60, 1),
        }
    })
    #return Response(resultado)