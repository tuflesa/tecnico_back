from rest_framework import viewsets
from mantenimiento.models import Notificacion
from mantenimiento.serializers import NotificacionSerializer
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

class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    queryset = Notificacion.objects.all()
    filterset_class = NotificacionFilter
