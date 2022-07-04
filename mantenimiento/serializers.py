from estructura.models import Seccion
from rest_framework import serializers
from django.db.models import fields
from django.db.models.base import Model
from mantenimiento.models import Especialidad, Notificacion, ParteTrabajo, Tarea, TipoPeriodo, TipoTarea, LineaParteTrabajo, EstadoLineasTareas, TrabajadoresLineaParte
from administracion.serializers import UserSerializer
from estructura.serializers import EquipoSerializer, SeccionSerializer, ZonaSerializer

class NotificacionSerializer(serializers.ModelSerializer):
    quien = UserSerializer(many=False)
    #para = UserSerializer(many=False)
    #fecha_creacion = serializers.DateField(format="%d-%m-%Y")
    class Meta:
        model = Notificacion
        fields = ['id', 'numero', 'que', 'cuando', 'donde', 'quien', 'como', 'cuanto', 'porque', 'empresa', 'fecha_creacion', 'revisado', 'descartado', 'finalizado', 'conclusion']

class NotificacionNuevaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'numero', 'que', 'cuando', 'donde', 'quien', 'como', 'cuanto', 'porque', 'empresa', 'fecha_creacion', 'revisado', 'descartado', 'finalizado', 'conclusion']


class TipoPeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPeriodo
        fields = ['id', 'nombre', 'cantidad_dias']
class TareaSerializer(serializers.ModelSerializer):
    tipo_periodo = TipoPeriodoSerializer()
    class Meta:
        model = Tarea
        fields = ['id', 'nombre', 'especialidad', 'prioridad', 'observaciones', 'especialidad_nombre', 'periodo', 'tipo_periodo']

class TareaEditarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id', 'nombre', 'especialidad', 'prioridad', 'observaciones', 'especialidad_nombre', 'periodo', 'tipo_periodo']

class TareaNuevaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id', 'nombre', 'especialidad', 'prioridad', 'observaciones', 'especialidad_nombre', 'tipo_periodo', 'periodo']

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ['id', 'nombre']

class TipoTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTarea
        fields = ['id', 'nombre']
class EstadoLineasTareasSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoLineasTareas
        fields = ['id', 'nombre']

class ParteTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParteTrabajo
        fields = ['id', 'nombre', 'tipo', 'creado_por', 'observaciones', 'finalizado', 'fecha_creacion', 'fecha_finalizacion', 'equipo', 'tipo_nombre', 'fecha_prevista_inicio', 'zona', 'seccion', 'empresa', 'tarea', 'estado', 'num_parte']

class ParteTrabajoDetalleSerializer(serializers.ModelSerializer):
    equipo = EquipoSerializer(many=False, read_only=True)
    seccion = SeccionSerializer(many=False, read_only=True)
    creado_por = UserSerializer(many=False, read_only=True)
    tarea = TareaSerializer(many=True, read_only=True)
    class Meta:
        model = ParteTrabajo
        fields = ['id', 'nombre', 'tipo', 'creado_por', 'observaciones', 'finalizado', 'fecha_creacion', 'fecha_finalizacion', 'equipo', 'tipo_nombre', 'fecha_prevista_inicio', 'zona', 'seccion', 'empresa', 'tarea', 'estado', 'estado_nombre', 'num_parte']

class PartesFiltradosSerializer(serializers.ModelSerializer):
    equipo = EquipoSerializer(many=False, read_only=True)
    seccion = SeccionSerializer(many=False, read_only=True)
    creado_por = UserSerializer(many=False, read_only=True)
    tarea = TareaSerializer(many=True, read_only=True)
    class Meta:
        model = ParteTrabajo
        fields = ['id', 'nombre', 'tipo', 'creado_por', 'observaciones', 'finalizado', 'fecha_creacion', 'fecha_finalizacion', 'equipo', 'tipo_nombre', 'fecha_prevista_inicio', 'zona', 'seccion', 'empresa', 'tarea', 'estado', 'estado_nombre', 'num_parte']

class ParteTrabajoEditarSerializer(serializers.ModelSerializer):
    equipo = EquipoSerializer(many=False, read_only=True)
    seccion = SeccionSerializer(many=False, read_only=True)
    creado_por = UserSerializer(many=False, read_only=True)
    tarea = TareaEditarSerializer(many=True, read_only=True)
    class Meta:
        model = ParteTrabajo
        fields = ['id', 'nombre', 'tipo', 'creado_por', 'observaciones', 'finalizado', 'fecha_creacion', 'fecha_finalizacion', 'equipo', 'tipo_nombre', 'fecha_prevista_inicio', 'zona', 'seccion', 'empresa', 'tarea', 'estado', 'estado_nombre', 'num_parte']

class LineaParteTrabajoSerializer(serializers.ModelSerializer):
    #parte = ParteTrabajoDetalleSerializer(many=False, read_only=True)
    tarea = TareaSerializer(many=False, read_only=True)
    class Meta:
        model = LineaParteTrabajo
        fields = ['id', 'parte', 'tarea', 'fecha_inicio', 'fecha_fin', 'estado', 'fecha_plan']

class LineaParteTrabajoMovSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaParteTrabajo
        fields = ['id', 'parte', 'tarea', 'fecha_inicio', 'fecha_fin', 'estado', 'fecha_plan']

class LineaParteTrabajoNuevaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaParteTrabajo
        fields = ['id', 'parte', 'tarea', 'fecha_inicio', 'fecha_fin', 'estado', 'fecha_plan']

class ListadoLineasPartesSerializer(serializers.ModelSerializer):
    parte = ParteTrabajoDetalleSerializer(many=False, read_only=True)
    tarea = TareaSerializer(many=False, read_only=True)
    class Meta:
        model = LineaParteTrabajo
        fields = ['id', 'parte', 'tarea', 'fecha_inicio', 'fecha_fin', 'estado', 'fecha_plan']

class ListadoLineasActivasSerializer(serializers.ModelSerializer):
    parte = ParteTrabajoDetalleSerializer(many=False, read_only=True)
    tarea = TareaSerializer(many=False, read_only=True)
    class Meta:
        model = LineaParteTrabajo
        fields = ['id', 'parte', 'tarea', 'fecha_inicio', 'fecha_fin', 'estado', 'fecha_plan']

class TrabajadoresLineaParteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrabajadoresLineaParte
        fields = ['id', 'linea', 'fecha_inicio', 'fecha_fin', 'trabajador']

class TrabajadoresEnLineaSerializer(serializers.ModelSerializer):
    trabajador = UserSerializer(many=False, read_only=True)
    class Meta:
        model = TrabajadoresLineaParte
        fields = ['id', 'linea', 'fecha_inicio', 'fecha_fin', 'trabajador']