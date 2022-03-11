from rest_framework import viewsets
from mantenimiento.models import Notificacion, ParteTrabajo, Tarea, Especialidad, TipoPeriodo, TipoTarea, LineaParteTrabajo
from mantenimiento.serializers import NotificacionSerializer, TareaSerializer, EspecialidadSerializer, TipoTareaSerializer, TipoPeriodoSerializer, TareaNuevaSerializer, ParteTrabajoSerializer, ParteTrabajoDetalleSerializer, LineaParteTrabajoSerializer, LineaParteTrabajoNuevaSerializer, LineaParteTrabajoMovSerializer
from django_filters import rest_framework as filters
from django.db.models import Count, F, Value

class NotificacionFilter(filters.FilterSet):
    class Meta:
        model = Notificacion
        fields = {
            'empresa': ['exact'],
            'que': ['icontains'],
            'revisado': ['exact'],
            'descartado': ['exact'],
            'finalizado': ['exact'],
            
        }
class TareaFilter(filters.FilterSet):
    class Meta:
        model = Tarea
        fields = {
            'nombre': ['icontains'],
            'especialidad': ['exact'],
            'prioridad': ['lte', 'gte'],
        }

class LineasFilter(filters.FilterSet):
    class Meta:
        model = LineaParteTrabajo
        fields = {
            'parte': ['exact'],
            'tarea': ['exact'],
        }

class EspecialidadFilter(filters.FilterSet):
    class Meta:
        model = Especialidad
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

class TareaNuevaViewSet(viewsets.ModelViewSet):
    serializer_class = TareaNuevaSerializer
    queryset = Tarea.objects.all()
    filterset_class = TareaFilter

class TipoTareaViewSet(viewsets.ModelViewSet):
    serializer_class = TipoTareaSerializer
    queryset = TipoTarea.objects.all()

class TipoPeriodoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoPeriodoSerializer
    queryset = TipoPeriodo.objects.all()

class LineaParteTrabajoViewSet(viewsets.ModelViewSet):
    serializer_class = LineaParteTrabajoSerializer
    queryset = LineaParteTrabajo.objects.all().distinct()
    filterset_class = LineasFilter

class LineaParteTrabajoMovViewSet(viewsets.ModelViewSet):
    serializer_class = LineaParteTrabajoMovSerializer
    queryset = LineaParteTrabajo.objects.all()
    filterset_class = LineasFilter

class LineaParteTrabajoNuevaViewSet(viewsets.ModelViewSet):
    serializer_class = LineaParteTrabajoNuevaSerializer
    queryset = LineaParteTrabajo.objects.all()

class ParteTrabajoViewSet(viewsets.ModelViewSet):
    serializer_class = ParteTrabajoSerializer
    #queryset = ParteTrabajo.objects.filter(tareas__gt=0)
    queryset = ParteTrabajo.objects.all()
    filterset_class = PartesFilter

class ParteTrabajoDetalleViewSet(viewsets.ModelViewSet):
    serializer_class = ParteTrabajoDetalleSerializer
    queryset = ParteTrabajo.objects.all()
    filterset_class = PartesFilter