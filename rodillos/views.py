from rest_framework import viewsets
from rodillos.models import Rodillo, Tipo_rodillo, Seccion, Operacion, Eje, Plano, Revision
from rodillos.serializers import RodilloSerializer, PlanoSerializer, RevisionSerializer
from django_filters import rest_framework as filters

class RodilloFilter(filters.FilterSet):
    class Meta:
        model = Rodillo
        fields = {
            'nombre': ['exact'],
        }

class RodilloViewSet(viewsets.ModelViewSet):
    serializer_class = RodilloSerializer
    queryset = Rodillo.objects.all()
    filterset_class = RodilloFilter

class PlanoViewSet(viewsets.ModelViewSet):
    serializer_class = PlanoSerializer
    queryset = Plano.objects.all()

class RevisionViewSet(viewsets.ModelViewSet):
    serializer_class = RevisionSerializer
    queryset = Revision.objects.all()


