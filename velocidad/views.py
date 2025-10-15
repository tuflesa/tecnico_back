from rest_framework import viewsets
from django.http import JsonResponse
from django_filters import rest_framework as filters
from .serializers import RegistroSerializer, ZonaPerfilVelocidadSerilizer
from .models import Registro, ZonaPerfilVelocidad
from estructura.models import Zona
from trazabilidad.models import Flejes
from django.forms.models import model_to_dict
from django.db.models import Q

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
    fecha = request.GET.get('fecha')
    hora_inicio = request.GET.get('hora_inicio')
    hora_fin = request.GET.get('hora_fin')

    # Datos de la máquina
    maquina = Zona.objects.get(id=id)
    maquina_dict = model_to_dict(maquina)


    # Registros de velocidad
    registros = Registro.objects.filter(
        fecha=fecha,
        hora__gte=hora_inicio,
        hora__lte=hora_fin,
        zona=id
    )

    velocidad = [{
        'fecha': r.fecha.isoformat(),
        'hora': r.hora.isoformat(),
        'zona': r.zona.siglas,
        'velocidad':  float(r.velocidad)
    } for r in registros]

    # Flejes fabricados
    # Condición 1: fecha_entrada >= fecha y hora_entrada >= hora_inicio
    # Condición 2: fecha_salida <= fecha y hora_salida <= hora_fin
    resultado = Flejes.objects.filter(
        Q(fecha_entrada=fecha, hora_entrada__gte=hora_inicio) |
        Q(fecha_salida=fecha, hora_salida__lte=hora_fin)
    ).order_by('fecha_entrada', 'hora_entrada')
    # Serializar resultados
    flejes = [{
        'id': f.id,
        'idProduccion': f.idProduccion,
        'IdArticulo': f.IdArticulo,
        'peso': f.peso,
        'of': f.of,
        'maquina_siglas': f.maquina_siglas,
        'fecha_entrada': f.fecha_entrada.isoformat() if f.fecha_entrada else None,
        'hora_entrada': f.hora_entrada.isoformat() if f.hora_entrada else None,
        'fecha_salida': f.fecha_salida.isoformat() if f.fecha_salida else None,
        'hora_salida': f.hora_salida.isoformat() if f.hora_salida else None,
        'finalizada': f.finalizada
    } for f in resultado]

    data = {
        "maquina": maquina_dict,
        "velocidad": velocidad,
        "flejes": flejes
    }
    return JsonResponse(data)