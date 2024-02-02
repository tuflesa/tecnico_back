from rest_framework import viewsets
from rodillos.models import Rodillo, Tipo_rodillo, Seccion, Operacion, Eje, Plano, Revision, Material, Grupo, Tipo_Plano, Nombres_Parametros, Tipo_Seccion, Parametros_Estandar, Bancada, Conjunto, Elemento, Celda, Forma
from rodillos.serializers import RodilloSerializer, PlanoNuevoSerializer, RevisionSerializer, SeccionSerializer, OperacionSerializer, TipoRodilloSerializer, MaterialSerializer, GrupoSerializer, TipoPlanoSerializer, RodilloListSerializer, PlanoParametrosSerializer, Nombres_ParametrosSerializer, TipoSeccionSerializer, PlanoSerializer, RevisionConjuntosSerializer, Parametros_estandarSerializer, Plano_existenteSerializer, EjeSerializer, BancadaSerializer, ConjuntoSerializer, ElementoSerializer, Elemento_SelectSerializer, Bancada_GruposSerializer, Bancada_SelectSerializer, CeldaSerializer, Celda_SelectSerializer, Grupo_onlySerializer, FormaSerializer, Celda_DuplicarSerializer, Bancada_CTSerializer
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    paginator=1
    max_page_size = 1000 

class ConjuntoFilter(filters.FilterSet):
    class Meta:
        model = Conjunto
        fields = {
            'tubo_madre': ['exact'],
            'operacion': ['exact'],
        }

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
            'operacion__seccion__tipo':['exact'],
            'operacion__nombre': ['exact'],
            'nombre': ['icontains'],
            'tipo':['exact'],
            'operacion__seccion__maquina__empresa__id': ['exact'],
            'operacion__seccion__maquina': ['exact'],
            'operacion__seccion': ['exact'],
            'operacion__id':['exact'],
            'tipo_plano':['exact'],
            'grupo':['exact'],
        }

class CeldaFilter(filters.FilterSet):
    class Meta:
        model = Celda
        fields = {
            'bancada__seccion__maquina__id': ['exact'],
            'bancada__seccion__maquina__id': ['exact'],
            'bancada__tubo_madre':['exact'],
            'bancada__dimensiones':['exact'],
            'bancada__seccion__maquina__empresa':['exact'],
            'bancada__seccion__pertenece_grupo':['exact'],
            'conjunto__id':['exact'],
            'bancada__id':['exact'],
            'bancada__dimensiones':['exact'],
            'conjunto__operacion':['exact'],
        }

class CeldaDuplicarFilter(filters.FilterSet):
    class Meta:
        model = Celda
        fields = {
            'bancada':['exact'],
            'bancada__id':['exact'],
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
            'pertenece_grupo':['exact'],
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
            'seccion__pertenece_grupo':['exact'],
        }

class Tipo_rodilloFilter(filters.FilterSet):
    class Meta:
        model = Tipo_rodillo
        fields = {
            'nombre': ['exact'],
        }

class EjeFilter(filters.FilterSet):
    class Meta:
        model = Eje
        fields = {
            'operacion': ['exact'],
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
            'nombre': ['icontains'],
            'maquina': ['exact'],
            'tubo_madre': ['exact'],
            'maquina__siglas': ['exact'],
            'maquina__id':['exact'],
            'maquina__empresa': ['exact'],
        }

class ElementoFilter(filters.FilterSet):
    class Meta:
        model = Elemento
        fields = {
            'id': ['exact'],
            'eje': ['exact'],
            'rodillo': ['exact'],
            'conjunto': ['exact'],
            'conjunto__tubo_madre':['exact'],
            'conjunto__operacion':['exact'],
            'conjunto__id':['exact'],
        }

class BancadaFilter(filters.FilterSet):
    class Meta:
        model = Bancada
        fields = {
            'seccion': ['exact'],
            'tubo_madre': ['exact'],
            'seccion__nombre':['exact'],
            'tubo_madre': ['lte', 'gte'],
        }

class BancadaCTFilter(filters.FilterSet):
    class Meta:
        model = Bancada
        fields = {
            'seccion': ['exact'],
            'seccion__maquina__id': ['exact'],
            'seccion__maquina__empresa':['exact'],
            'dimensiones': ['icontains'],
            'seccion__pertenece_grupo':['exact'],
        }

class BancadaGrupoFilter(filters.FilterSet):
    class Meta:
        model = Bancada
        fields = {
            'seccion': ['exact'],
            'tubo_madre': ['exact'],
            'seccion__nombre':['exact'],
            'dimensiones':['exact'],
        }

class FormaFilter(filters.FilterSet):
    class Meta:
        model = Forma
        fields = {
            'nombre': ['exact'],
        }

class Grupo_NuevoViewSet(viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all()
    filterset_class = GrupoFilter

class GrupoViewSet(viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all()
    filterset_class = GrupoFilter
    pagination_class = StandardResultsSetPagination

class Grupo_onlyViewSet(viewsets.ModelViewSet):
    serializer_class = Grupo_onlySerializer
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
            'rodillos__operacion__seccion__maquina__siglas': ['exact'],
            'rodillos__operacion__seccion__maquina__id': ['exact'],
            'rodillos__operacion__seccion__nombre': ['exact'],
            'rodillos__tipo':['exact'],
            'rodillos__operacion__id': ['exact'],
        }

class Tipo_PlanoFilter(filters.FilterSet):
    class Meta:
        model = Tipo_Plano
        fields = {
            'nombre': ['exact'],
            'tipo_seccion':['exact'],
            'tipo_rodillo': ['exact'],
            'id':['exact'],
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
    queryset = Rodillo.objects.all().order_by('-grupo')
    filterset_class = RodilloFilter
    pagination_class = StandardResultsSetPagination

class Rodillo_existenteViewSet(viewsets.ModelViewSet):
    serializer_class = RodilloListSerializer
    queryset = Rodillo.objects.all().order_by('-grupo','tipo')
    filterset_class = RodilloFilter

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
    queryset = Seccion.objects.all().order_by('orden')
    filterset_class = SeccionFilter

class Operacion_CTViewSet(viewsets.ModelViewSet):#ESTO MEJOR PARA MONTAR CT FILTRANDO AL REVÉS
    serializer_class = OperacionSerializer
    queryset = Operacion.objects.filter(seccion__tipo=5).order_by('orden')
    filterset_class = OperacionFilter

class OperacionViewSet(viewsets.ModelViewSet):
    serializer_class = OperacionSerializer
    queryset = Operacion.objects.all().order_by('orden')
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
    queryset = Plano.objects.all().order_by('nombre').distinct()
    filterset_class = PlanoFilter

class EjeViewSet(viewsets.ModelViewSet):
    serializer_class = EjeSerializer
    queryset = Eje.objects.all()
    filterset_class = EjeFilter

class BancadaViewSet(viewsets.ModelViewSet):
    serializer_class = BancadaSerializer
    queryset = Bancada.objects.all().order_by('tubo_madre')
    filterset_class = BancadaFilter
    
class BancadaCTViewSet(viewsets.ModelViewSet):
    serializer_class = Bancada_CTSerializer
    queryset = Bancada.objects.all().order_by('dimensiones')
    filterset_class = BancadaCTFilter
    pagination_class = StandardResultsSetPagination
class BancadaGruposViewSet(viewsets.ModelViewSet):
    serializer_class = Bancada_GruposSerializer
    queryset = Bancada.objects.all()
    filterset_class = BancadaGrupoFilter

class ConjuntoViewSet(viewsets.ModelViewSet):
    serializer_class = ConjuntoSerializer
    queryset = Conjunto.objects.all()
    filterset_class = ConjuntoFilter

class ElementoViewSet(viewsets.ModelViewSet):
    serializer_class = ElementoSerializer
    queryset = Elemento.objects.all()
    filterset_class = ElementoFilter

class Elemento_SelectViewSet(viewsets.ModelViewSet):
    queryset = Elemento.objects.all()
    serializer_class = Elemento_SelectSerializer
    filterset_class = ElementoFilter

class Bancada_SelectViewSet(viewsets.ModelViewSet):
    serializer_class = Bancada_SelectSerializer
    queryset = Bancada.objects.all()
    #filterset_class = BancadaFilter

class Celda_SelectViewSet(viewsets.ModelViewSet):
    serializer_class = Celda_SelectSerializer
    queryset = Celda.objects.all().order_by('conjunto__operacion')
    filterset_class = CeldaFilter

class CeldaViewSet(viewsets.ModelViewSet):
    serializer_class = CeldaSerializer
    queryset = Celda.objects.all()
    filterset_class = CeldaFilter

class Celda_DuplicarViewSet(viewsets.ModelViewSet):
    serializer_class = Celda_DuplicarSerializer
    queryset = Celda.objects.all().order_by('conjunto__operacion')
    filterset_class = CeldaDuplicarFilter

class FormaViewSet(viewsets.ModelViewSet):
    serializer_class = FormaSerializer
    queryset = Forma.objects.all()
    filterset_class = FormaFilter