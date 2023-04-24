# from asyncio.windows_events import NULL
from rest_framework import viewsets
from mantenimiento.models import Notificacion, ParteTrabajo, Tarea, Especialidad, TipoPeriodo, TipoTarea, LineaParteTrabajo, EstadoLineasTareas, TrabajadoresLineaParte, Reclamo
from mantenimiento.serializers import LineasDeUnTrabajadorSerializer, PartesFiltradosSerializer, ParteTrabajoEditarSerializer, NotificacionSerializer, NotificacionNuevaSerializer, TareaSerializer, EspecialidadSerializer, TipoTareaSerializer, TipoPeriodoSerializer, TareaNuevaSerializer, ParteTrabajoSerializer, ParteTrabajoDetalleSerializer, LineaParteTrabajoSerializer, LineaParteTrabajoNuevaSerializer, LineaParteTrabajoMovSerializer, ListadoLineasPartesSerializer, EstadoLineasTareasSerializer, TrabajadoresLineaParteSerializer, ListadoLineasActivasSerializer, TrabajadoresEnLineaSerializer,  ReclamoSerializer
from django_filters import rest_framework as filters
from django.db.models import Count, F, Value
from rest_framework.pagination import PageNumberPagination

class NotificacionFilter(filters.FilterSet):
    class Meta:
        model = Notificacion
        fields = {
            'empresa__id': ['exact'],
            'que': ['icontains'],
            'revisado': ['exact'],
            'descartado': ['exact'],
            'finalizado': ['exact'],
            'quien' :['exact'],
            'fecha_creacion' : ['lte', 'gte'], 
            'zona__id' : ['exact'],
            'numero' : ['icontains'],
            'zona__nombre':['exact'],
        }
class TareaFilter(filters.FilterSet):
    class Meta:
        model = Tarea
        fields = {
            'nombre': ['icontains'],
            'especialidad': ['exact'],
            'prioridad': ['lte', 'gte'],  
            'id': ['exact'],
            'tipo_periodo' : ['exact'],     
        }

class LineasFilter(filters.FilterSet):
    class Meta:
        model = LineaParteTrabajo
        fields = {
            'parte': ['exact'],
            'tarea': ['exact'],            
            'tarea__nombre': ['icontains'],
            'tarea__especialidad': ['exact'],
            'tarea__prioridad': ['lte', 'gte'],
            'parte__tipo': ['exact'],
            'parte__empresa' : ['exact'],
            'parte__empresa__id' : ['exact'],
            'parte__zona__id': ['exact'],
            'parte__seccion__id': ['exact'],
            'parte__equipo__id': ['exact'],
            'parte__nombre': ['icontains'],
            'fecha_inicio': ['lte', 'gte'],
            'fecha_fin': ['lte', 'gte'],
            'fecha_plan': ['lte', 'gte'],
            'estado': ['exact'],
            'id': ['exact'],
            'parte__zona' : ['exact'],
            'parte__seccion' : ['exact'],
            'parte__equipo' : ['exact'],
            'tarea__id' : ['exact'],
            'fecha_fin': ['exact'],
            'tarea__tipo_periodo__cantidad_dias' : ['exact'],

        }

class EspecialidadFilter(filters.FilterSet):
    class Meta:
        model = Especialidad
        fields = {
            'nombre': ['icontains'],
            'nombre': ['exact'],
            'id': ['exact'],
        }

class TipoPeriodoFilter(filters.FilterSet):
    class Meta:
        model = TipoPeriodo
        fields = {
            'nombre': ['icontains'],
        }

class PartesFilter(filters.FilterSet):
    class Meta:
        model = ParteTrabajo
        fields = {
            'nombre': ['icontains'],
            'tipo': ['exact'],
            'creado_por':['exact'],
            'observaciones': ['icontains'],
            'finalizado': ['exact'],
            'empresa__id' : ['exact'],
            'zona__id': ['exact'],
            'seccion__id': ['exact'],
            'equipo__id': ['exact'],
            'fecha_prevista_inicio': ['lte', 'gte'],
            'estado': ['exact'],
            'num_parte': ['icontains'],
            'tarea__id': ['exact'],
            'fecha_finalizacion': ['exact'],
            'fecha_finalizacion': ['lte', 'gte'],
        }

class EstadoLineasTareasFilter(filters.FilterSet):
    class Meta:
        model = EstadoLineasTareas
        fields = {
            'nombre': ['exact'],
        }

class TrabajadoresLineaParteFilter(filters.FilterSet):
    class Meta:
        model = TrabajadoresLineaParte
        fields = {
            'trabajador': ['exact'],
            'linea': ['exact'],
            'fecha_inicio': ['lte', 'gte'],
            'fecha_fin': ['lte', 'gte'],
            'linea__parte__empresa': ['exact'],
        }

class ReclamoFilter(filters.FilterSet):
    class Meta:
        model = Reclamo
        fields = {
            'notificacion': ['exact'],
            'trabajador': ['exact'],
            'fecha': ['lte', 'gte'],
        }

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    paginator=1
    max_page_size = 1000 

class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    queryset = Notificacion.objects.all().order_by('-id')
    filterset_class = NotificacionFilter
    pagination_class = StandardResultsSetPagination

class Notificacion_sinpaginarViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    queryset = Notificacion.objects.all().order_by('-id')
    filterset_class = NotificacionFilter

class NotificacionNuevaViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionNuevaSerializer
    queryset = Notificacion.objects.all()
    filterset_class = NotificacionFilter

class EspecialidadViewSet(viewsets.ModelViewSet):
    serializer_class = EspecialidadSerializer
    queryset = Especialidad.objects.all()
    filterset_class = EspecialidadFilter
class TipoPeriodoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoPeriodoSerializer
    queryset = TipoPeriodo.objects.all()
    filterset_class = TipoPeriodoFilter

class EstadoLineasTareasViewSet(viewsets.ModelViewSet):
    serializer_class = EstadoLineasTareasSerializer
    queryset = EstadoLineasTareas.objects.all()
    filterset_class = EstadoLineasTareasFilter

class TareaViewSet(viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    queryset = Tarea.objects.all().distinct()
    filterset_class = TareaFilter

class TareaNuevaViewSet(viewsets.ModelViewSet):
    serializer_class = TareaNuevaSerializer
    queryset = Tarea.objects.all()
    filterset_class = TareaFilter

class TipoTareaViewSet(viewsets.ModelViewSet):
    serializer_class = TipoTareaSerializer
    queryset = TipoTarea.objects.all().order_by('nombre')
class LineaParteTrabajoViewSet(viewsets.ModelViewSet):
    serializer_class = LineaParteTrabajoSerializer
    queryset = LineaParteTrabajo.objects.all()
    filterset_class = LineasFilter

class LineaParteTrabajoMovViewSet(viewsets.ModelViewSet):
    serializer_class = LineaParteTrabajoMovSerializer
    queryset = LineaParteTrabajo.objects.all()
    filterset_class = LineasFilter

class LineaParteTrabajoNuevaViewSet(viewsets.ModelViewSet):
    serializer_class = LineaParteTrabajoNuevaSerializer
    queryset = LineaParteTrabajo.objects.all()
    filterset_class = LineasFilter

class ListadoLineaParteViewSet(viewsets.ModelViewSet):
    serializer_class = ListadoLineasPartesSerializer
    queryset = LineaParteTrabajo.objects.all().order_by('-tarea__prioridad')
    filterset_class = LineasFilter
    pagination_class = StandardResultsSetPagination

#excluimos de la busqueda aquellas con estado 3 = finalizadas y 4 = pendientes
class ListadoLineaActivasViewSet(viewsets.ModelViewSet):
    serializer_class = ListadoLineasActivasSerializer
    queryset = LineaParteTrabajo.objects.exclude(estado=3).exclude(estado=4).order_by('-tarea__prioridad')
    filterset_class = LineasFilter
    pagination_class = StandardResultsSetPagination


#excluimos de la busqueda aquellas con estado 3 = finalizadas y 4 = pendientes
class ListadoLineaActivasSinPaginarViewSet(viewsets.ModelViewSet):
    serializer_class = ListadoLineasActivasSerializer
    queryset = LineaParteTrabajo.objects.exclude(estado=3).exclude(estado=4).order_by('-tarea__prioridad')
    filterset_class = LineasFilter

class ParteTrabajoViewSet(viewsets.ModelViewSet):
    serializer_class = ParteTrabajoSerializer
    #queryset = ParteTrabajo.objects.filter(tareas__gt=0)
    queryset = ParteTrabajo.objects.all()
    filterset_class = PartesFilter

class ParteTrabajoDetalleViewSet(viewsets.ModelViewSet):
    serializer_class = ParteTrabajoDetalleSerializer
    queryset = ParteTrabajo.objects.all().order_by('id')
    filterset_class = PartesFilter
    pagination_class = StandardResultsSetPagination
    
#excluimos de la busqueda aquellas con estado 3 = finalizadas y 4 = pendientes
class ParteActivosTrabajoViewSet(viewsets.ModelViewSet):
    serializer_class = ParteTrabajoDetalleSerializer
    queryset = ParteTrabajo.objects.exclude(estado=3).exclude(estado=4).order_by('-id')
    filterset_class = PartesFilter
    pagination_class = StandardResultsSetPagination

class PartesFiltradosViewSet(viewsets.ModelViewSet):
    serializer_class = PartesFiltradosSerializer
    queryset = ParteTrabajo.objects.filter(estado=3).filter(fecha_finalizacion=None)
    filterset_class = PartesFilter

class ParteTrabajoEditarViewSet(viewsets.ModelViewSet):
    serializer_class = ParteTrabajoEditarSerializer
    queryset = ParteTrabajo.objects.all()
    filterset_class = PartesFilter

class TrabajadoresLineaParteViewSet(viewsets.ModelViewSet):
    serializer_class = TrabajadoresLineaParteSerializer
    queryset = TrabajadoresLineaParte.objects.all()
    filterset_class = TrabajadoresLineaParteFilter

class TrabajadoresLineaParteFechaNullViewSet(viewsets.ModelViewSet):
    serializer_class = TrabajadoresLineaParteSerializer
    queryset = TrabajadoresLineaParte.objects.filter(fecha_fin=None)
    filterset_class = TrabajadoresLineaParteFilter

class TrabajadoresEnLineaViewSet(viewsets.ModelViewSet):
    serializer_class = TrabajadoresEnLineaSerializer
    queryset = TrabajadoresLineaParte.objects.all()
    filterset_class = TrabajadoresLineaParteFilter

class LineasdeunTrabajadorViewSet(viewsets.ModelViewSet):
    serializer_class = LineasDeUnTrabajadorSerializer
    queryset = TrabajadoresLineaParte.objects.all().order_by('-linea__parte')
    filterset_class = TrabajadoresLineaParteFilter
    pagination_class = StandardResultsSetPagination

class ReclamoViewSet(viewsets.ModelViewSet):
    serializer_class = ReclamoSerializer
    queryset = Reclamo.objects.all()
    filterset_class = ReclamoFilter