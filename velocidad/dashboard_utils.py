# dashboard_utils.py
from datetime import date
from django.utils import timezone
from estructura.models import Zona

def _clamp(value, lo, hi):
    return max(lo, min(hi, value))

def _segundos(inicio, fin):
    return max(0.0, (fin - inicio).total_seconds())

def _siglas_zona(zona_id):
    return Zona.objects.get(id=zona_id).siglas.upper()

def _clave_agrupacion(fecha, agrupar):
    if isinstance(fecha, str):
        fecha = date.fromisoformat(fecha)
    if agrupar == 'mes':
        return fecha.strftime('%Y-%m')
    elif agrupar == 'rango':
        return 'rango'
    return fecha.strftime('%Y-%m-%d')