from rest_framework import viewsets
from rodillos.models import Rodillo, Tipo_rodillo, Seccion, Operacion, Eje, Plano, Revision, Material, Grupo, Tipo_Plano
from rodillos.serializers import RodilloSerializer, PlanoSerializer, RevisionSerializer, SeccionSerializer, OperacionSerializer, TipoRodilloSerializer, MaterialSerializer, GrupoSerializer, TipoPlanoSerializer, RodilloListSerializer
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    paginator=1
    max_page_size = 1000 

class RodilloFilter(filters.FilterSet):
    class Meta:
        model = Rodillo
        fields = {
            'nombre': ['exact'],
            'id': ['exact'],
            'operacion': ['exact'],
            'operacion__seccion__nombre': ['exact'],
            'operacion__seccion__maquina__siglas': ['exact'],
            'operacion__seccion__maquina__empresa__nombre': ['exact'],
            'operacion__nombre': ['exact'],
        }

class SeccionFilter(filters.FilterSet):
    class Meta:
        model = Seccion
        fields = {
            'nombre': ['exact'],
            'maquina__siglas': ['exact'],
            'maquina__empresa__siglas': ['exact'],
        }

class OperacionFilter(filters.FilterSet):
    class Meta:
        model = Operacion
        fields = {
            'nombre': ['exact'],
            'seccion': ['exact'],
            'seccion__nombre': ['exact'],
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
            'id': ['exact'],
            'nombre': ['exact'],
            'maquina': ['exact'],
            'tubo_madre': ['exact'],
        }

class GrupoViewSet(viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all()
    filterset_class = GrupoFilter
    
class PlanoFilter(filters.FilterSet):
    class Meta:
        model = Plano
        fields = {
            'nombre': ['exact'],
        }

class Tipo_PlanoFilter(filters.FilterSet):
    class Meta:
        model = Tipo_Plano
        fields = {
            'nombre': ['exact'],
        }
class RodilloViewSet(viewsets.ModelViewSet):
    serializer_class = RodilloSerializer
    queryset = Rodillo.objects.all()
    filterset_class = RodilloFilter

class Rodillo_listViewSet(viewsets.ModelViewSet):
    serializer_class = RodilloListSerializer
    queryset = Rodillo.objects.all()
    filterset_class = RodilloFilter
    pagination_class = StandardResultsSetPagination

class PlanoViewSet(viewsets.ModelViewSet):
    serializer_class = PlanoSerializer
    queryset = Plano.objects.all()
    filterset_class = PlanoFilter

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

class TipoPlanoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoPlanoSerializer
    queryset = Tipo_Plano.objects.all()
    filterset_class = Tipo_PlanoFilter


