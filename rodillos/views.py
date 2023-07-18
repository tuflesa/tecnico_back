from rest_framework import viewsets
from rodillos.models import Rodillo, Tipo_rodillo, Seccion, Operacion, Eje, Plano, Revision, Material, Grupo
from rodillos.serializers import RodilloSerializer, PlanoSerializer, RevisionSerializer, SeccionSerializer, OperacionSerializer, TipoRodilloSerializer, MaterialSerializer, GrupoSerializer
from django_filters import rest_framework as filters

class RodilloFilter(filters.FilterSet):
    class Meta:
        model = Rodillo
        fields = {
            'nombre': ['exact'],
        }

class SeccionFilter(filters.FilterSet):
    class Meta:
        model = Seccion
        fields = {
            'nombre': ['exact'],
            'maquina': ['exact'],
        }

class OperacionFilter(filters.FilterSet):
    class Meta:
        model = Operacion
        fields = {
            'nombre': ['exact'],
            'seccion': ['exact'],
        }

class Tipo_rodilloFilter(filters.FilterSet):
    class Meta:
        model = Tipo_rodillo
        fields = {
            'nombre': ['exact'],
        }
    
class MaterialFilter(filters.FilterSet):
    class Meta:
        model = Material
        fields = {
            'nombre': ['exact'],
        }

class GrupoFilter(filters.FilterSet):
    class Meta:
        model = Grupo
        fields = {
            'nombre': ['exact'],
            'maquina': ['exact'],
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

class SeccionViewSet(viewsets.ModelViewSet):
    serializer_class = SeccionSerializer
    queryset = Seccion.objects.all()
    filterset_class = SeccionFilter

class OperacionViewSet(viewsets.ModelViewSet):
    serializer_class = OperacionSerializer
    queryset = Operacion.objects.all()
    filterset_class = OperacionFilter

class TipoRodilloViewSet(viewsets.ModelViewSet):
    serializer_class = TipoRodilloSerializer
    queryset = Tipo_rodillo.objects.all()
    filterset_class = Tipo_rodilloFilter

class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    filterset_class = MaterialFilter

class GrupoViewSet(viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all()
    filterset_class = GrupoFilter


