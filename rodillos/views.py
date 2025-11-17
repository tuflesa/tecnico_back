from rest_framework import status, viewsets
from rodillos.models import Rodillo, Tipo_rodillo, Seccion, Operacion, Eje, Plano, Revision, Material, Grupo, Tipo_Plano, Nombres_Parametros, Tipo_Seccion, Parametros_Estandar, Bancada, Conjunto, Elemento, Celda, Forma, Montaje, Icono, Instancia, Rectificacion, LineaRectificacion, Posicion, Icono_celda, Anotaciones
from rodillos.serializers import RodilloSerializer, PlanoNuevoSerializer, RevisionSerializer, SeccionSerializer, OperacionSerializer, TipoRodilloSerializer, MaterialSerializer, GrupoSerializer, TipoPlanoSerializer, RodilloListSerializer, PlanoParametrosSerializer, Nombres_ParametrosSerializer, TipoSeccionSerializer, PlanoSerializer, RevisionConjuntosSerializer, Parametros_estandarSerializer, Plano_existenteSerializer, EjeSerializer, BancadaSerializer, ConjuntoSerializer, ElementoSerializer, Elemento_SelectSerializer, Bancada_GruposSerializer, Bancada_SelectSerializer, CeldaSerializer, Celda_SelectSerializer, Grupo_onlySerializer, FormaSerializer, Celda_DuplicarSerializer, Bancada_CTSerializer, MontajeSerializer, MontajeListadoSerializer, MontajeToolingSerializer, RodillosSerializer, Conjunto_OperacionSerializer, RevisionPlanosSerializer, IconoSerializer, EjeOperacionSerializer, InstanciaSerializer, InstanciaListadoSerializer, RectificacionSerializer, RectificacionListaSerializer, LineaRectificacionSerializer, ListadoLineaRectificacionSerializer, PosicionSerializer, MontajeQSSerializer, Icono_celdaSerializer, BancadaQSSerializer, CeldaQSSerializer, AnotacionesSerializer, LineaRectificacion_toolingSerializer, Celda_programadoresSerializer
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q, Value, CharField
from django.db.models.functions import Concat
from rest_framework.decorators import action
from django.db.models import Max
from ftplib import FTP
from django.db.models import Count
import django_filters
class EliminarViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='eliminar_archivos')
    def eliminar_archivos(self, request):
        servidor = "10.10.20.51"  # Dirección del servidor FTP
        usuario = "domenem"            # Usuario FTP
        contrasena = "Domenada77"      # Contraseña FTP
        carpeta = "/"                     # Carpeta en el servidor (puedes especificar una ruta)

        try:
            # Conexión al servidor FTP
            with FTP(servidor) as ftp:
                ftp.login(usuario, contrasena)
                ftp.cwd(carpeta)  # Cambiar al directorio deseado

                # Listar y eliminar todos los archivos en la carpeta
                archivos = ftp.nlst()  # Lista de archivos en el directorio
                for archivo in archivos:
                    try:
                        ftp.delete(archivo)  # Eliminar archivo
                    except Exception as e:
                        return Response({"error": f"No se pudo eliminar {archivo}: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response({"message": f"Contenido de {carpeta} eliminado exitosamente."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Error al conectar o eliminar archivos en el servidor FTP: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    paginator=1
    max_page_size = 1000 

class ListadoLineaRectificacionFilter(filters.FilterSet):
    full_name = filters.CharFilter(method='filter_full_name')    
    class Meta:
        model = LineaRectificacion
        fields = {
            'rectificado': ['exact'],
            'rectificado__id': ['exact'],
            'instancia__id': ['exact'],
            'instancia__rodillo__operacion__id':['exact'],
            'instancia__rodillo__operacion__seccion__id':['exact'],
            'instancia__rodillo__operacion__seccion__maquina__id':['exact'],
            'instancia__rodillo__operacion__seccion__maquina__empresa__id':['exact'],
            'instancia__nombre': ['icontains'],
            'finalizado':['exact'],
            'rectificado_por':['exact'],
            'proveedor': ['exact'],
        }

    def filter_full_name(self, queryset, name, value):
        return queryset.annotate(
            full_name=Concat('rectificado_por__first_name', Value(' '), 'rectificado_por__last_name', output_field=CharField())
        ).filter(full_name__icontains=value)
class RectificacionesListadoFilter(filters.FilterSet):
    full_name = filters.CharFilter(method='filter_full_name')
    proveedor = filters.CharFilter(method='filter_proveedor')
    class Meta:
        model = Rectificacion
        fields = {
            'id': ['exact'],
            'empresa': ['exact'],
            'maquina__id': ['exact'],
            'numero': ['icontains'],
            'creado_por':['exact'],
            'finalizado' : ['exact'],
            'proveedor': ['exact'],
        }
    def filter_full_name(self, queryset, name, value):
        return queryset.annotate(
            full_name=Concat('creado_por__first_name', Value(' '), 'creado_por__last_name', output_field=CharField())
        ).filter(full_name__icontains=value)
    def filter_proveedor(self, queryset, name, value):
        if value == 'sin_proveedor':
            # Filtrar los registros donde proveedor es nulo
            return queryset.filter(proveedor__isnull=True)
        elif value:
            # Filtrar por proveedor específico
            return queryset.filter(**{name: value})
        # Si no hay filtro de proveedor (opción "Todas" o vacío)
        return queryset

class RectificacionesFilter(filters.FilterSet):
    class Meta:
        model = Rectificacion
        fields = {
            'id': ['exact'],
        }
class ConjuntoFilter(filters.FilterSet):
    class Meta:
        model = Conjunto
        fields = {
            'tubo_madre': ['exact'],
            'operacion': ['exact'],
        }

class ConjuntoOperacionFilter(filters.FilterSet):
    class Meta:
        model = Conjunto
        fields = {
            'tubo_madre': ['exact'],
            'operacion': ['exact'],
            'operacion__seccion__id':['exact'],
            'operacion__id': ['exact'],
            'tubo_madre': ['lte', 'gte'],
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
            'grupo__tubo_madre':['exact'],
            'nombre':['icontains'],
            'num_instancias':['exact'],
        }

class RodillosFilter(filters.FilterSet):
    class Meta:
        model = Rodillo
        fields = {
            'operacion__id':['exact'],
            'grupo__id':['exact'],
            'nombre':['exact'],
            'grupo__tubo_madre':['exact'],
            'es_generico': ['exact'],
        }

class InstanciaFilter(filters.FilterSet):
    class Meta:
        model = Instancia
        fields = {
            'rodillo':['exact'],
        }

class InstanciaListadoFilter(filters.FilterSet):
    class Meta:
        model = Instancia
        fields = {
            'rodillo__id':['exact'],
            'obsoleta':['exact'],
            'id':['exact'],
            'rodillo__operacion__seccion__maquina__id':['exact'],
            'rodillo__operacion__seccion__id':['exact'],
            'nombre':['icontains'],
            'rodillo__operacion__id':['exact'],

        }
class CeldaFilter(filters.FilterSet):
    icono_isnull = django_filters.BooleanFilter(field_name='icono', lookup_expr='isnull')
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
            'bancada':['exact'],
            'operacion':['exact'],
            'icono': ['exact'],
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
    posiciones_count = django_filters.NumberFilter(field_name='posiciones_count', lookup_expr='exact')
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
            'icono__id':['exact'],
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

class EjeOperacionFilter(filters.FilterSet):
    class Meta:
        model = Eje
        fields = {
            'operacion__seccion__maquina__id': ['exact'],
            'operacion__id': ['exact'],
            'tipo':['exact'],
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
            'plano':['exact'],
        }

class RevisionPlanosFilter(filters.FilterSet):
    class Meta:
        model = Revision
        fields = {
            'plano__id':['exact'],
            'plano__nombre':['exact'],
            'plano__rodillos':['exact'],
            'plano__xa_rectificado':['exact'],
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
            'tubo_madre': ['lte', 'gte'],
            'maquina__siglas': ['exact'],
            'maquina__id':['exact'],
            'maquina__empresa': ['exact'],
            'tubo_madre': ['lte', 'gte'],
        }

class GrupoNuevoFilter(filters.FilterSet):
    class Meta:
        model = Grupo
        fields = {
            'id': ['exact'],
            'nombre': ['exact'],
            'maquina': ['exact'],
            'tubo_madre': ['exact'],
            'maquina__siglas': ['exact'],
            'maquina__id':['exact'],
            'maquina__empresa': ['exact'],
            'espesor_1': ['exact'],
            'espesor_2': ['exact'],
        }

class ElementoFilter(filters.FilterSet):
    class Meta:
        model = Elemento
        fields = {
            'id': ['exact'],
            'eje': ['exact'],
            'rodillo': ['exact'],
            'rodillo__id': ['exact'],
            'conjunto': ['exact'],
            'conjunto__tubo_madre':['exact'],
            'conjunto__operacion':['exact'],
            'conjunto__id':['exact'],
        }

class ElementoSelectFilter(filters.FilterSet):
    class Meta:
        model = Elemento
        fields = {
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
            'seccion__maquina__empresa__id':['exact'],
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
            'seccion__maquina':['exact'],
        }

class FormaFilter(filters.FilterSet):
    class Meta:
        model = Forma
        fields = {
            'nombre': ['exact'],
        }

class MontajeFilter(filters.FilterSet):
    class Meta:
        model = Montaje
        fields = {
            'grupo': ['exact'],
            'bancadas':['exact'],
            'maquina':['exact'],
            'bancadas__id':['exact'],
        }

class MontajeListadoFilter(filters.FilterSet):
    class Meta:
        model = Montaje
        fields = {
            'grupo__id': ['exact'],
            'maquina__id':['exact'],
            'bancadas__id':['exact'],
            'nombre':['icontains'],
            'maquina__empresa__id': ['exact'],
        }

class IconoCeldaFilter(filters.FilterSet):
    class Meta:
        model = Icono_celda
        fields = {
            'pertenece_grupo': ['exact'],
            'pertenece_ct': ['exact'],
        }

class AnotacionesFilter(filters.FilterSet):
    class Meta:
        model = Anotaciones
        fields = {
            'montaje': ['exact'],
        }

class Grupo_NuevoViewSet(viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all().order_by('tubo_madre')
    filterset_class = GrupoNuevoFilter

class grupo_montajeViewSet(viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all().order_by('nombre')
    filterset_class = GrupoFilter

class GrupoViewSet(viewsets.ModelViewSet):
    serializer_class = GrupoSerializer
    queryset = Grupo.objects.all().order_by('nombre')
    filterset_class = GrupoFilter
    pagination_class = StandardResultsSetPagination

class Grupo_onlyViewSet(viewsets.ModelViewSet):
    serializer_class = Grupo_onlySerializer
    queryset = Grupo.objects.all().order_by('tubo_madre')
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
            'cod_antiguo': ['icontains'],
            'descripcion': ['icontains'],
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

class RodillosViewSet(viewsets.ModelViewSet):
    serializer_class = RodillosSerializer
    queryset = Rodillo.objects.all()
    filterset_class = RodillosFilter

class Rodillo_listViewSet(viewsets.ModelViewSet):
    serializer_class = RodilloListSerializer
    queryset = Rodillo.objects.all().order_by('-grupo__nombre','operacion__orden')
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

class RevisionPlanosViewSet(viewsets.ModelViewSet):
    serializer_class = RevisionPlanosSerializer
    queryset = Revision.objects.all().order_by('-id')
    filterset_class = RevisionPlanosFilter

class RevisionPlanosRecienteViewSet(viewsets.ViewSet):
    serializer_class = RevisionPlanosSerializer

    def list(self, request):
        rodillo_id = request.query_params.get('plano__rodillos')
        xa_rectificado_str = request.query_params.get('plano__xa_rectificado')
        xa_rectificado = xa_rectificado_str.lower() == 'true' if xa_rectificado_str is not None else None # Convertir el valor de xa_rectificado a un booleano
        # Filtrado según los parámetros
        subquery  = Revision.objects.filter(
            plano__rodillos=rodillo_id,
            plano__xa_rectificado=xa_rectificado
        ).values('plano_id').annotate(max_id=Max('id')).values_list('max_id', flat=True)

        queryset = Revision.objects.filter(id__in=subquery).order_by('-id')

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
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
    queryset = Seccion.objects.all().order_by('maquina','orden')
    filterset_class = SeccionFilter

class Operacion_CTViewSet(viewsets.ModelViewSet):#ESTO MEJOR PARA MONTAR CT FILTRANDO AL REVÉS
    serializer_class = OperacionSerializer
    queryset = Operacion.objects.filter(seccion__pertenece_grupo=False).order_by('orden')
    filterset_class = OperacionFilter

class OperacionViewSet(viewsets.ModelViewSet):
    serializer_class = OperacionSerializer
    queryset = Operacion.objects.annotate(posiciones_count=Count('posiciones')).order_by('orden')
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

class EjeOperacionViewSet(viewsets.ModelViewSet):
    serializer_class = EjeOperacionSerializer
    queryset = Eje.objects.all().order_by('diametro')
    filterset_class = EjeOperacionFilter

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
    queryset = Bancada.objects.all().order_by('tubo_madre')
    filterset_class = BancadaGrupoFilter

class BancadaMontajeCTViewSet(viewsets.ModelViewSet):
    serializer_class = Bancada_GruposSerializer
    queryset = Bancada.objects.exclude(dimensiones__isnull=True).order_by('dimensiones')
    filterset_class = BancadaGrupoFilter

class BancadaMontajeViewSet(viewsets.ModelViewSet):
    serializer_class = Bancada_GruposSerializer
    queryset = Bancada.objects.all()
    filterset_class = BancadaGrupoFilter

class ConjuntoViewSet(viewsets.ModelViewSet):
    serializer_class = ConjuntoSerializer
    queryset = Conjunto.objects.all()
    filterset_class = ConjuntoFilter

class Conjunto_OperacionViewSet(viewsets.ModelViewSet):
    serializer_class = Conjunto_OperacionSerializer
    queryset = Conjunto.objects.none()  # solo para evitar el error del router

    def get_queryset(self):
        queryset = Conjunto.objects.select_related('operacion').annotate(
            posiciones_count=Count('operacion__posiciones')
        )

        # Filtros individuales
        posiciones_count = self.request.query_params.get('posiciones_count')
        if posiciones_count:
            queryset = queryset.filter(posiciones_count=posiciones_count)

        seccion_id = self.request.query_params.get('operacion__seccion__id')
        if seccion_id:
            queryset = queryset.filter(operacion__seccion__id=seccion_id)

        operacion_id = self.request.query_params.get('operacion__id')
        if operacion_id:
            queryset = queryset.filter(operacion__id=operacion_id)

        tubo_madre_gte = self.request.query_params.get('tubo_madre__gte')
        if tubo_madre_gte:
            queryset = queryset.filter(tubo_madre__gte=tubo_madre_gte)

        tubo_madre_lte = self.request.query_params.get('tubo_madre__lte')
        if tubo_madre_lte:
            queryset = queryset.filter(tubo_madre__lte=tubo_madre_lte)

        return queryset.order_by('operacion')

class ElementoViewSet(viewsets.ModelViewSet):
    serializer_class = ElementoSerializer
    queryset = Elemento.objects.all()
    filterset_class = ElementoFilter

class Elemento_SelectViewSet(viewsets.ModelViewSet):
    queryset = Elemento.objects.all()
    serializer_class = Elemento_SelectSerializer
    filterset_class = ElementoSelectFilter

class Bancada_SelectViewSet(viewsets.ModelViewSet):
    serializer_class = Bancada_SelectSerializer
    queryset = Bancada.objects.all()
    #filterset_class = BancadaFilter

class Icono_celdaViewSet(viewsets.ModelViewSet):
    serializer_class = Icono_celdaSerializer
    queryset = Icono_celda.objects.all()
    filterset_class = IconoCeldaFilter

class Celda_SelectViewSet(viewsets.ModelViewSet):
    serializer_class = Celda_SelectSerializer
    queryset = Celda.objects.all().order_by('conjunto__operacion')
    filterset_class = CeldaFilter
class Celda_programadoresViewSet(viewsets.ModelViewSet):
    serializer_class = Celda_programadoresSerializer
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

class MontajeViewSet(viewsets.ModelViewSet):
    serializer_class = MontajeSerializer
    queryset = Montaje.objects.all()
    filterset_class = MontajeFilter

class MontajeListadoViewSet(viewsets.ModelViewSet):
    serializer_class = MontajeListadoSerializer
    queryset = Montaje.objects.all().order_by('nombre')
    filterset_class = MontajeListadoFilter
    pagination_class = StandardResultsSetPagination
class MontajeQSViewSet(viewsets.ModelViewSet):
    serializer_class = MontajeQSSerializer
    queryset = Montaje.objects.all().order_by('nombre')
    filterset_class = MontajeListadoFilter
class MontajeToolingViewSet(viewsets.ModelViewSet):
    serializer_class = MontajeToolingSerializer
    queryset = Montaje.objects.all()
    filterset_class = MontajeListadoFilter
class IconoViewSet(viewsets.ModelViewSet):
    serializer_class = IconoSerializer
    queryset = Icono.objects.all()

class InstanciaViewSet(viewsets.ModelViewSet):
    serializer_class = InstanciaSerializer
    queryset = Instancia.objects.all()
    filterset_class = InstanciaFilter

class InstanciaListadoViewSet(viewsets.ModelViewSet):
    serializer_class = InstanciaListadoSerializer
    queryset = Instancia.objects.all()
    filterset_class = InstanciaListadoFilter

class RectificacionViewSet(viewsets.ModelViewSet):
    serializer_class = RectificacionSerializer
    queryset = Rectificacion.objects.all()
    filterset_class = RectificacionesFilter

class RectificacionListaViewSet(viewsets.ModelViewSet):
    serializer_class = RectificacionListaSerializer
    queryset = Rectificacion.objects.all()
    filterset_class = RectificacionesListadoFilter
    pagination_class = StandardResultsSetPagination

class LineaRectificacionViewSet(viewsets.ModelViewSet):
    serializer_class = LineaRectificacionSerializer
    queryset = LineaRectificacion.objects.all()

class LineaRectificaciontoolingViewSet(viewsets.ModelViewSet):
    serializer_class = LineaRectificacion_toolingSerializer
    queryset = LineaRectificacion.objects.filter(finalizado=False)
class ListadoLineaRectificacionViewSet(viewsets.ModelViewSet):
    serializer_class = ListadoLineaRectificacionSerializer
    queryset = LineaRectificacion.objects.all().order_by('-fecha_rectificado','fecha','id')
    filterset_class = ListadoLineaRectificacionFilter

class PosicionViewSet(viewsets.ModelViewSet):
    serializer_class = PosicionSerializer
    queryset = Posicion.objects.all()

class CeldaQSViewSet(viewsets.ModelViewSet):
    serializer_class = CeldaQSSerializer
    queryset = Celda.objects.all()
    filterset_class = CeldaFilter

class AnotacionesViewSet(viewsets.ModelViewSet):
    serializer_class = AnotacionesSerializer
    queryset = Anotaciones.objects.all()
    filterset_class = AnotacionesFilter