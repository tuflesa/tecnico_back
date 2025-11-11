from rest_framework import viewsets
from django.http import JsonResponse
from django_filters import rest_framework as filters
from .serializers import RegistroSerializer, ZonaPerfilVelocidadSerilizer
from .models import Registro, ZonaPerfilVelocidad
from estructura.models import Zona
from trazabilidad.models import Flejes
from django.forms.models import model_to_dict
from django.db.models import Q
from datetime import datetime, time

class RegistroFilter(filters.FilterSet):
    class Meta:
        model = Registro
        fields = {
            'zona__empresa': ['exact'],
            'fecha': ['exact'],
            'hora': ['gte', 'lte']
        }

class ZonaPerfilVelocidadFilter(filters.FilterSet):
    class Meta:
        model = ZonaPerfilVelocidad
        fields = {
            'zona__empresa': ['exact'],
            'id': ['exact'],
        }

class ZonaPerfilVelocidadViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ZonaPerfilVelocidadSerilizer
    queryset = ZonaPerfilVelocidad.objects.all()
    filterset_class = ZonaPerfilVelocidadFilter

class RegistroViewSet(viewsets.ModelViewSet):
    serializer_class = RegistroSerializer
    queryset = Registro.objects.all().order_by('fecha', 'hora')
    filterset_class = RegistroFilter

def estado_maquina(request, id):
    fecha_str = request.GET.get('fecha')
    hora_inicio_str = request.GET.get('hora_inicio')
    hora_fin_str = request.GET.get('hora_fin')

    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
        hora_fin = datetime.strptime(hora_fin_str, '%H:%M').time()
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Formato de hora inválido'}, status=400)


    # Datos de la máquina
    zona = Zona.objects.get(id=id)
    maquina = ZonaPerfilVelocidad.objects.get(zona=zona)
    maquina_dict = model_to_dict(maquina)
    zona_dict = model_to_dict(zona)
    maquina_dict['zona'] = zona_dict


    # Registros de velocidad
    from itertools import chain

    # Consulta principal
    registros = Registro.objects.filter(
        fecha=fecha,
        hora__gte=hora_inicio,
        hora__lte=hora_fin,
        zona=id
    ).order_by('hora')

    # Obtener el registro anterior si hay resultados
    anterior = Registro.objects.filter(
        zona=id
        ).filter(
            # Fecha anterior o misma fecha con hora menor
            Q(fecha__lt=fecha) |
            Q(fecha=fecha, hora__lt=hora_inicio)
        ).order_by('-fecha', '-hora').first()

    if anterior:
        registros = list(chain([anterior], registros))

    regs = [{
        'fecha': r.fecha.isoformat(),
        'hora': r.hora.isoformat(),
        'zona': r.zona.siglas,
        'velocidad':  float(r.velocidad),
        'potencia': float(r.potencia),
        'frecuencia': float(r.frecuencia),
        'presion': float(r.presion)
    } for r in registros]

    # Flejes fabricados
    siglas = maquina.zona.siglas.upper()
    resultado = Flejes.objects.filter(
        Q(maquina_siglas=siglas, fecha_entrada=fecha, hora_entrada__range=[hora_inicio, hora_fin]) | 
        Q(maquina_siglas=siglas, fecha_salida=fecha, hora_salida__range=[hora_inicio, hora_fin]) |
        Q(maquina_siglas=siglas, fecha_entrada=fecha, hora_entrada__gte=hora_inicio, fecha_salida__isnull=True, hora_salida__isnull=True)
    ).distinct().order_by('-fecha_entrada', '-hora_entrada')
    # Serializar resultados
    flejes = [{
        'id': f.id,
        'pos': f.pos,
        'idProduccion': f.idProduccion,
        'IdArticulo': f.IdArticulo,
        'peso': f.peso,
        'of': f.of,
        'maquina_siglas': f.maquina_siglas,
        'descripcion': f.descripcion,
        'fecha_entrada': f.fecha_entrada.isoformat() if f.fecha_entrada else None,
        'hora_entrada': f.hora_entrada.isoformat() if f.hora_entrada else None,
        'fecha_salida': f.fecha_salida.isoformat() if f.fecha_salida else None,
        'hora_salida': f.hora_salida.isoformat() if f.hora_salida else None,
        'finalizada': f.finalizada,
        'ancho': f.ancho(),
        'espesor': f.espesor(),
        'metros_teorico': f.metros_teorico(),
        'metros_medido': f.metros_medido,
        'metros_tubo': f.metros_tubo(),
        'tubos': [{
            'n_tubos': t.n_tubos,
            'largo': t.largo
        } for t in f.tubos.all()]
    } for f in resultado]

    # Estado actual
    estado_act = Registro.objects.filter(zona=id).last()
    fleje_act = Flejes.objects.filter(maquina_siglas=siglas, fecha_salida__isnull=True).order_by('-fecha_entrada', '-hora_entrada').last()
    if (fleje_act == None):
        from types import SimpleNamespace
        fleje_act = SimpleNamespace(
            of='',
            pos='',
            descripcion=''
        )


    estado_act = {
        'velocidad':  float(estado_act.velocidad),
        'potencia': float(estado_act.potencia),
        'frecuencia': float(estado_act.frecuencia),
        'fuerza': float(estado_act.presion),
        'of': fleje_act.of,
        'fleje_pos': fleje_act.pos,
        'fleje_descripcion': fleje_act.descripcion
    }

    data = {
        "maquina": maquina_dict,
        "registros": regs,
        "flejes": flejes,
        "estado_act": estado_act
    }
    return JsonResponse(data)