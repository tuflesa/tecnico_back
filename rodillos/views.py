from rest_framework import viewsets
from rodillos.models import Rodillo, Tipo_rodillo, Seccion, Operacion, Eje, Plano, Revision, Tipo_Plano, Grupo, Material
from rodillos.serializers import RodilloSerializer, PlanoSerializer, RevisionSerializer, TipoPlanoSerializer, SeccionSerializer, OperacionSerializer, GrupoSerializer, Tipo_rodilloSerializer, MaterialSerializer
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

class TipoPlanoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoPlanoSerializer
    queryset = Tipo_Plano.objects.all()

class SeccionViewSet(viewsets.ModelViewSet):
    serializer_class = SeccionSerializer
    queryset = Seccion.objects.all()

class OperacionViewSet(viewsets.ModelViewSet):
    serializer_class = OperacionSerializer
    queryset = Operacion.objects.all()

class Tipo_rodilloViewSet(viewsets.ModelViewSet):
    serializer_class = Tipo_rodilloSerializer
    queryset = Tipo_rodillo.objects.all()

class GrupoViewSet(viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all()

class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()


