# velocidad/dashboard_paradas.py

from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from datetime import datetime, date
from collections import defaultdict
import datetime as dt

from velocidad.models import Parada
from .dashboard_utils import _clamp, _segundos, _clave_agrupacion

# ─── Constantes ───────────────────────────────────────────────────────────────

TIPOS_PARADA = ('Incidencia', 'Avería')

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _minutos(seg):
    return round(seg / 60, 1)

def _acumulador_vacio():
    """{ palabra_clave: { TOTAL: {seg, n}, A: {seg, n}, B: {seg, n} } }"""
    return defaultdict(lambda: {
        'TOTAL': {'seg': 0.0, 'n': 0},
        'A':     {'seg': 0.0, 'n': 0},
        'B':     {'seg': 0.0, 'n': 0},
    })


def _construir_qs(zona_id, dt_desde, dt_hasta, tipo_nombre):
    return (
        Parada.objects
        .filter(zona_id=zona_id)
        .filter(codigo__tipo__nombre=tipo_nombre)
        .filter(
            Q(periodos__inicio__gte=dt_desde, periodos__inicio__lte=dt_hasta) |
            Q(periodos__fin__gte=dt_desde,    periodos__fin__lte=dt_hasta)
        )
        .prefetch_related('periodos__turno', 'codigo__palabra_clave')
        .distinct()
    )


def _distribuir(paradas_qs, dt_desde, dt_hasta, turnos_cfg):
    """
    Devuelve: dict[palabra_clave_nombre] → { TOTAL, A, B } con seg y n.
    Agrupa siempre por rango completo (no por día ni mes).
    """
    acc = _acumulador_vacio()

    for parada in paradas_qs:
        pc = parada.codigo.palabra_clave
        if not pc:
            continue
        pc_nombre = pc.nombre

        periodos_validos = []

        # Paso 1: acumular segundos
        for periodo in parada.periodos.all():
            if not periodo.inicio:
                continue

            fin_real = periodo.fin if periodo.fin else timezone.now()
            p_ini    = _clamp(periodo.inicio, dt_desde, dt_hasta)
            p_fin    = _clamp(fin_real,       dt_desde, dt_hasta)

            if p_fin <= p_ini:
                continue

            turno_letra = periodo.turno.turno if periodo.turno else 'X'
            seg = _segundos(p_ini, p_fin)
            periodos_validos.append((p_ini, p_fin, turno_letra))

            acc[pc_nombre]['TOTAL']['seg'] += seg
            if turno_letra in turnos_cfg:
                acc[pc_nombre][turno_letra]['seg'] += seg

        if not periodos_validos:
            continue

        # Paso 2: contar n
        acc[pc_nombre]['TOTAL']['n'] += 1

        turnos_con_seg = set()
        for p_ini, p_fin, turno_letra in periodos_validos:
            if turno_letra not in turnos_cfg:
                continue
            if _segundos(p_ini, p_fin) > 0:
                turnos_con_seg.add(turno_letra)

        for turno_letra in turnos_con_seg:
            acc[pc_nombre][turno_letra]['n'] += 1

    return acc


def _serializar(acc):
    """Convierte el acumulador, en lista ordenada por tiempo total descendiente."""
    resultado = []
    for pc_nombre, turnos in acc.items():
        resultado.append({
            'palabra_clave': pc_nombre,
            'total':         _minutos(turnos['TOTAL']['seg']),
            'total_n':       turnos['TOTAL']['n'],
            'turno_a':       _minutos(turnos['A']['seg']),
            'turno_a_n':     turnos['A']['n'],
            'turno_b':       _minutos(turnos['B']['seg']),
            'turno_b_n':     turnos['B']['n'],
        })
    return sorted(resultado, key=lambda x: x['total'], reverse=True)


# ─── Vista ────────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def paradas_palabraclave(request):
    """
    Gráficos 1 y 2: tiempo parado por palabra clave, separado por tipo.
    Params: zona_id, fecha_desde, fecha_hasta, turnos (lista)
    Respuesta: {
        incidencia: [ { palabra_clave, total, turno_a, turno_b, ..._n } ],
        averia:     [ { palabra_clave, total, turno_a, turno_b, ..._n } ],
    }
    """
    zona_id     = request.GET.get('zona_id')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
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

    resultado = {}
    for tipo in TIPOS_PARADA:
        qs  = _construir_qs(zona_id, dt_desde, dt_hasta, tipo)
        acc = _distribuir(qs, dt_desde, dt_hasta, turnos_cfg)
        # clave del JSON: 'incidencia' / 'averia'
        clave = tipo.lower().replace('í', 'i').replace('é', 'e')
        resultado[clave] = _serializar(acc)

    return Response(resultado)

# ── idem _construir_qs pero con código ────────────────────────────────

def _construir_qs_codigo(zona_id, dt_desde, dt_hasta, tipo_nombre):
    """
    Igual que _construir_qs pero agrupa por CodigoParada.nombre en vez de palabra_clave.
    """
    return (
        Parada.objects
        .filter(zona_id=zona_id)
        .filter(codigo__tipo__nombre=tipo_nombre)
        .filter(
            Q(periodos__inicio__gte=dt_desde, periodos__inicio__lte=dt_hasta) |
            Q(periodos__fin__gte=dt_desde,    periodos__fin__lte=dt_hasta)
        )
        .prefetch_related('periodos__turno', 'codigo')
        .distinct()
    )


def _distribuir_codigo(paradas_qs, dt_desde, dt_hasta, turnos_cfg):
    """
    Igual que _distribuir pero agrupa por CodigoParada.nombre en vez de palabra_clave.
    """
    acc = _acumulador_vacio()

    for parada in paradas_qs:
        codigo_nombre = parada.codigo.nombre
        periodos_validos = []

        for periodo in parada.periodos.all():
            if not periodo.inicio:
                continue

            fin_real = periodo.fin if periodo.fin else timezone.now()
            p_ini    = _clamp(periodo.inicio, dt_desde, dt_hasta)
            p_fin    = _clamp(fin_real,       dt_desde, dt_hasta)

            if p_fin <= p_ini:
                continue

            turno_letra = periodo.turno.turno if periodo.turno else 'X'
            seg = _segundos(p_ini, p_fin)
            periodos_validos.append((p_ini, p_fin, turno_letra))

            acc[codigo_nombre]['TOTAL']['seg'] += seg
            if turno_letra in turnos_cfg:
                acc[codigo_nombre][turno_letra]['seg'] += seg

        if not periodos_validos:
            continue

        acc[codigo_nombre]['TOTAL']['n'] += 1

        turnos_con_seg = set()
        for p_ini, p_fin, turno_letra in periodos_validos:
            if turno_letra not in turnos_cfg:
                continue
            if _segundos(p_ini, p_fin) > 0:
                turnos_con_seg.add(turno_letra)

        for turno_letra in turnos_con_seg:
            acc[codigo_nombre][turno_letra]['n'] += 1

    return acc


def _serializar_codigo(acc):
    resultado = []
    for codigo_nombre, turnos in acc.items():
        resultado.append({
            'codigo':    codigo_nombre,
            'total':     _minutos(turnos['TOTAL']['seg']),
            'total_n':   turnos['TOTAL']['n'],
            'turno_a':   _minutos(turnos['A']['seg']),
            'turno_a_n': turnos['A']['n'],
            'turno_b':   _minutos(turnos['B']['seg']),
            'turno_b_n': turnos['B']['n'],
        })
    return sorted(resultado, key=lambda x: x['total'], reverse=True)


@api_view(['GET'])
@permission_classes([AllowAny])
def paradas_codigo(request):
    """
    Gráficos 3 y 4: tiempo parado por CodigoParada, separado por tipo.
    Parametros: zona_id, fecha_desde, fecha_hasta, turnos (lista)
    Respuesta en diccionarios: {
        incidencia: [ { codigo, total, turno_a, turno_b, ..._n } ],
        averia:     [ { codigo, total, turno_a, turno_b, ..._n } ],
    }
    """
    zona_id     = request.GET.get('zona_id')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
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

    resultado = {}
    for tipo in TIPOS_PARADA:
        qs    = _construir_qs_codigo(zona_id, dt_desde, dt_hasta, tipo)
        acc   = _distribuir_codigo(qs, dt_desde, dt_hasta, turnos_cfg)
        clave = tipo.lower().replace('í', 'i').replace('é', 'e')
        resultado[clave] = _serializar_codigo(acc)

    return Response(resultado)