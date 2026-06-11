# velocidad/dashboard_cambios.py

from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from datetime import datetime, date
from collections import defaultdict
import datetime as dt

from velocidad.models import Parada, HorarioDia
from .dashboard_utils import _clamp, _segundos, _siglas_zona, _clave_agrupacion

# ─── helpers propios de cambios ──────────────────────────────────────────────

TIPOS_CAMBIO = ('Cambio General', 'Cambio Parcial')

def _acumulador_vacio():
    """Estructura base por tipo de cambio."""
    return {
        'Cambio General': {'TOTAL': {'seg': 0.0, 'n': 0}, 'A': {'seg': 0.0, 'n': 0}, 'B': {'seg': 0.0, 'n': 0}},
        'Cambio Parcial': {'TOTAL': {'seg': 0.0, 'n': 0}, 'A': {'seg': 0.0, 'n': 0}, 'B': {'seg': 0.0, 'n': 0}},
    }

def _minutos(seg):
    return round(seg / 60, 1)

def _media_min(seg, n):
    if n == 0:
        return None
    return round((seg / n) / 60, 1)

def _serializar_grupo(acc, modo='suma'):
    """
    Convierte el acumulador en los 6 valores que devuelve el endpoint:
    cg_total, cg_A, cg_B, cp_total, cp_A, cp_B
    modo: 'suma' → minutos totales | 'media' → minutos medios por cambio
    """
    result = {}
    for tipo_key, tipo_label in [('Cambio General', 'cg'), ('Cambio Parcial', 'cp')]:
        for turno_key, turno_label in [('TOTAL', 'total'), ('A', 'turno_a'), ('B', 'turno_b')]:
            seg = acc[tipo_key][turno_key]['seg']
            n   = acc[tipo_key][turno_key]['n']
            if modo == 'suma':
                result[f'{tipo_label}_{turno_label}'] = _minutos(seg)
                result[f'{tipo_label}_{turno_label}_n'] = n
            else:
                result[f'{tipo_label}_{turno_label}'] = _media_min(seg, n)
                result[f'{tipo_label}_{turno_label}_n'] = n
    return result


def _construir_paradas_qs(zona_id, dt_desde, dt_hasta):
    return (
        Parada.objects
        .filter(zona_id=zona_id)
        .filter(codigo__nombre__in=TIPOS_CAMBIO)
        .filter(
            Q(periodos__inicio__gte=dt_desde, periodos__inicio__lte=dt_hasta) |
            Q(periodos__fin__gte=dt_desde,    periodos__fin__lte=dt_hasta)
        )
        .prefetch_related('periodos__turno', 'codigo')
        .distinct()
    )

def _distribuir_periodos(paradas_qs, dt_desde, dt_hasta, agrupar, turnos_cfg):
    """
    Recorre todas las paradas y acumula segundos + conteo por (clave, tipo_cambio, turno).
    Retorna: dict[clave] → acumulador_vacio relleno
    """
    grupos = defaultdict(_acumulador_vacio)

    for parada in paradas_qs:
        tipo_cambio = parada.codigo.nombre
        periodos_validos = []

        # ── Paso 1: recopilar periodos válidos y acumular segundos ────────
        for periodo in parada.periodos.all():
            if not periodo.inicio:
                continue

            fin_real     = periodo.fin if periodo.fin else timezone.now()
            p_ini        = _clamp(periodo.inicio, dt_desde, dt_hasta)
            p_fin        = _clamp(fin_real,       dt_desde, dt_hasta)

            if p_fin <= p_ini:
                continue

            turno_letra = periodo.turno.turno if periodo.turno else 'X'
            periodos_validos.append((p_ini, p_fin, turno_letra))

            # Acumular segundos dividiendo por días
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
                    grupos[clave][tipo_cambio]['TOTAL']['seg'] += seg
                    if turno_letra in turnos_cfg:
                        grupos[clave][tipo_cambio][turno_letra]['seg'] += seg
                actual = siguiente

        if not periodos_validos:
            continue

        # ── Paso 2: contar n ──────────────────────────────────────────────
        # TOTAL: 1 por parada, en la clave del primer periodo
        # En el total es 1 y en los turnos son 2 uno para cada turno (n difiere)
        clave_conteo = _clave_agrupacion(periodos_validos[0][0].date(), agrupar)
        grupos[clave_conteo][tipo_cambio]['TOTAL']['n'] += 1

        # Por turno: 1 por cada turno que tenga segundos en esta parada
        # Si un cambio cruza A y B, cuenta 1 en A y 1 en B
        # La media por turno = segundos de este cambio en ese turno / n de ese turno
        turnos_con_seg = set()
        for p_ini, p_fin, turno_letra in periodos_validos:
            if turno_letra not in turnos_cfg:
                continue
            if _segundos(p_ini, p_fin) > 0:
                turnos_con_seg.add((turno_letra, _clave_agrupacion(p_ini.date(), agrupar)))

        for turno_letra, clave_t in turnos_con_seg:
            grupos[clave_t][tipo_cambio][turno_letra]['n'] += 1

    return grupos
# ─── vista 1 y 2: suma y media por rango de fechas ───────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def cambios_rango(request):
    """
    Gráficos 1 y 2: suma y media de tiempos de cambio agrupados por intervalo.
    Parametros: zona_id, fecha_desde, fecha_hasta, agrupar (dia|mes|rango), turnos
    Respuesta: array de { periodo, suma: {...}, media: {...} }
    """
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

    paradas_qs = _construir_paradas_qs(zona_id, dt_desde, dt_hasta)
    grupos     = _distribuir_periodos(paradas_qs, dt_desde, dt_hasta, agrupar, turnos_cfg)

    resultado = []
    for clave in sorted(grupos.keys()): # Ordenamos la información para enviarla al frontend
        acc = grupos[clave]
        resultado.append({
            'periodo': clave,
            'suma':    _serializar_grupo(acc, modo='suma'),
            'media':   _serializar_grupo(acc, modo='media'),
        })

    return Response(resultado)


# ─── vista 3 y 4: anual por meses ────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def cambios_anual(request):
    """
    Gráficos 3 y 4: suma y media mensuales del año completo.
    Parametros: zona_id, anio (por defecto año actual), turnos
    Respuesta: array de 12 elementos { mes (YYYY-MM), suma: {...}, media: {...} }
    Misma lógica que cambios_rango con agrupar='mes' sobre el año entero.
    """
    zona_id    = request.GET.get('zona_id')
    anio       = int(request.GET.get('anio', datetime.now().year))
    turnos_cfg = request.GET.getlist('turnos') or ['A', 'B']

    if not zona_id:
        return Response({'error': 'zona_id es obligatorio'}, status=400)

    f_desde = date(anio, 1, 1)
    f_hasta = date(anio, 12, 31)

    dt_desde = timezone.make_aware(datetime.combine(f_desde, datetime.min.time()))
    dt_hasta = timezone.make_aware(datetime.combine(f_hasta, datetime.max.time()))

    # Usamos agrupar='mes' — misma función que el rango, misma lógica
    paradas_qs = _construir_paradas_qs(zona_id, dt_desde, dt_hasta)
    grupos     = _distribuir_periodos(paradas_qs, dt_desde, dt_hasta, 'mes', turnos_cfg)

    # Garantizar los 12 meses aunque no haya datos, aparecen a 0
    resultado = []
    for mes in range(1, 13):
        clave = f'{anio}-{mes:02d}'
        acc   = grupos.get(clave, _acumulador_vacio())
        resultado.append({
            'mes':   clave,
            'suma':  _serializar_grupo(acc, modo='suma'),
            'media': _serializar_grupo(acc, modo='media'),
        })

    return Response(resultado)