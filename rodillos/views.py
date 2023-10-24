from rest_framework import viewsets
from rodillos.models import Rodillo, Tipo_rodillo, Seccion, Operacion, Eje, Plano, Revision, Material, Grupo, Tipo_Plano, Nombres_Parametros, Tipo_Seccion, Parametros_Estandar
from rodillos.serializers import RodilloSerializer, PlanoNuevoSerializer, RevisionSerializer, SeccionSerializer, OperacionSerializer, TipoRodilloSerializer, MaterialSerializer, GrupoSerializer, TipoPlanoSerializer, RodilloListSerializer, PlanoParametrosSerializer, Nombres_ParametrosSerializer, TipoSeccionSerializer, PlanoSerializer, RevisionConjuntosSerializer, Parametros_estandarSerializer, Plano_existenteSerializer
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response

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
            'nombre': ['icontains'],
            'tipo':['exact'],
            'operacion__seccion__maquina__empresa__id': ['exact'],
            'operacion__seccion__maquina': ['exact'],
            'operacion__seccion': ['exact'],
            'operacion__id':['exact'],
            'tipo_plano':['exact'],
        }

class SeccionFilter(filters.FilterSet):
    class Meta:
        model = Seccion
        fields = {
            'nombre': ['exact'],
            'maquina__siglas': ['exact'],
            'maquina__empresa__siglas': ['exact'],
            'maquina__empresa__id': ['exact'],
            'maquina__id':['exact'],
            'maquina':['exact'],
        }

class OperacionFilter(filters.FilterSet):
    class Meta:
        model = Operacion
        fields = {
            'nombre': ['exact'],
            'nombre': ['icontains'],
            'seccion': ['exact'],
            'seccion__nombre': ['exact'],
            'seccion__id':['exact'],
            'seccion__maquina__siglas':['exact'],
            'seccion__maquina__empresa__id': ['exact'],
            'seccion__maquina': ['exact'],
            'seccion__maquina__id': ['exact'],
        }

class Tipo_rodilloFilter(filters.FilterSet):
    class Meta:
        model = Tipo_rodillo
        fields = {
            'nombre': ['exact'],
        }

class ParametrosFilter(filters.FilterSet):
    class Meta:
        model = Parametros_Estandar
        fields = {
            'rodillo': ['exact'],
            'nombre':['exact'],
            #'revision__plano__nombre': ['exact'],
        }

class RevisionFilter(filters.FilterSet):
    class Meta:
        model = Revision
        fields = {
            'plano__id': ['exact'],
            'plano':['exact'],
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
            'rodillos':['exact'],
            'nombre': ['icontains'],
            'rodillos__tipo_plano':['exact'],
        }

class Tipo_PlanoFilter(filters.FilterSet):
    class Meta:
        model = Tipo_Plano
        fields = {
            'nombre': ['exact'],
            'tipo_seccion':['exact'],
            'tipo_rodillo': ['exact'],
        }

class NombresParametrosFilter(filters.FilterSet):
    class Meta:
        model = Nombres_Parametros
        fields = {
            'nombre': ['exact'],
            'descripcion':['exact'],
            'id':['exact'],
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

class Rodillo_editarViewSet(viewsets.ModelViewSet):
    serializer_class = RodilloSerializer
    queryset = Rodillo.objects.all()
    filterset_class = RodilloFilter

class PlanoNuevoViewSet(viewsets.ModelViewSet):
    serializer_class = PlanoNuevoSerializer
    queryset = Plano.objects.all()
    filterset_class = PlanoFilter

class PlanoViewSet(viewsets.ModelViewSet):
    serializer_class = PlanoSerializer
    queryset = Plano.objects.all()
    filterset_class = PlanoFilter

class RevisionConjuntosViewSet(viewsets.ModelViewSet):
    serializer_class = RevisionConjuntosSerializer
    queryset = Revision.objects.all().order_by('-id')
    filterset_class = RevisionFilter
class RevisionViewSet(viewsets.ModelViewSet):
    serializer_class = RevisionSerializer
    queryset = Revision.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Obtener el archivo del formulario
            archivo = request.FILES.get('archivo')

            if archivo:
                # Procesar y guardar el archivo aquí
                nueva_revision = serializer.save(archivo=archivo)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'archivo': 'El archivo no se ha proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class Nombres_ParametrosViewSet(viewsets.ModelViewSet):
    serializer_class = Nombres_ParametrosSerializer
    queryset = Nombres_Parametros.objects.all()
    filterset_class = NombresParametrosFilter

class PlanoParametrosViewSet(viewsets.ModelViewSet):
    serializer_class = PlanoParametrosSerializer
    queryset = Tipo_Plano.objects.all()
    filterset_class = Tipo_PlanoFilter

class TipoSeccionViewSet(viewsets.ModelViewSet):
    serializer_class = TipoSeccionSerializer
    queryset = Tipo_Seccion.objects.all()

class Parametros_estandarViewSet(viewsets.ModelViewSet):
    serializer_class = Parametros_estandarSerializer
    queryset = Parametros_Estandar.objects.all()
    filterset_class = ParametrosFilter

class Plano_existenteViewSet(viewsets.ModelViewSet):
    serializer_class = Plano_existenteSerializer
    queryset = Plano.objects.all().order_by('nombre')
    filterset_class = PlanoFilter

