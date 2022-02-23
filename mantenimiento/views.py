from rest_framework import viewsets
from mantenimiento.models import Notificacion, Tarea, Especialidad
from mantenimiento.serializers import NotificacionSerializer, TareaSerializer, EspecialidadSerializer
from django_filters import rest_framework as filters

class NotificacionFilter(filters.FilterSet):
    class Meta:
        model = Notificacion
        fields = {
            'empresa': ['exact'],
            'que': ['icontains'],
            'revisado': ['exact'],
            'descartado': ['exact'],
            'finalizado': ['exact']
        }
class TareaFilter(filters.FilterSet):
    class Meta:
        model = Tarea
        fields = {
            'nombre': ['icontains'],
            'especialidad': ['exact'],
            'equipo__seccion__zona__empresa__id' : ['exact'],
        }

class EspecialidadFilter(filters.FilterSet):
    class Meta:
        model = Especialidad
        fields = {
            'nombre': ['icontains'],
        }

class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    queryset = Notificacion.objects.all()
    filterset_class = NotificacionFilter

class EspecialidadViewSet(viewsets.ModelViewSet):
    serializer_class = EspecialidadSerializer
    queryset = Especialidad.objects.all()
    filterset_class = EspecialidadFilter

class TareaViewSet(viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    queryset = Tarea.objects.all()
    filterset_class = TareaFilter
