from rest_framework import serializers
from django.db.models import fields
from django.db.models.base import Model
from mantenimiento.models import Especialidad, Notificacion, ParteTrabajo, Tarea, TipoPeriodo, TipoTarea, LineaParteTrabajo
from administracion.serializers import UserSerializer
from estructura.serializers import EquipoSerializer

class NotificacionSerializer(serializers.ModelSerializer):
    quien = UserSerializer(many=False)
    fecha_creacion = serializers.DateField(format="%d-%m-%Y")
    class Meta:
        model = Notificacion
        fields = ['id', 'numero', 'que', 'cuando', 'donde', 'quien', 'como', 'cuanto', 'porque', 'empresa', 'fecha_creacion', 'para', 'revisado', 'descartado', 'finalizado', 'conclusion']

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id', 'nombre', 'especialidad', 'prioridad', 'observaciones', 'especialidad_nombre']

class TareaNuevaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id', 'nombre', 'especialidad', 'prioridad', 'observaciones', 'especialidad_nombre']

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ['id', 'nombre']

class TipoTareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTarea
        fields = ['id', 'nombre']

class TipoPeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPeriodo
        fields = ['id', 'nombre']

class ParteTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParteTrabajo
        fields = ['id', 'nombre', 'tipo', 'creado_por', 'observaciones', 'finalizado', 'fecha_creacion', 'fecha_finalizacion', 'equipo', 'tipo_nombre', 'tipo_periodo', 'periodo', 'fecha_prevista_inicio', 'zona', 'seccion', 'empresa', 'tarea']

class ParteTrabajoDetalleSerializer(serializers.ModelSerializer):
    #equipo = EquipoSerializer(many=False, read_only=True)
    creado_por = UserSerializer(many=False, read_only=True)
    tarea = TareaSerializer(many=True, read_only=True)
    class Meta:
        model = ParteTrabajo
        fields = ['id', 'nombre', 'tipo', 'creado_por', 'observaciones', 'finalizado', 'fecha_creacion', 'fecha_finalizacion', 'equipo', 'tipo_nombre', 'tipo_periodo', 'periodo', 'fecha_prevista_inicio', 'zona', 'seccion', 'empresa', 'tarea']

class LineaParteTrabajoSerializer(serializers.ModelSerializer):
    #parte = ParteTrabajoDetalleSerializer(many=False, read_only=True)
    tarea = TareaSerializer(many=False, read_only=True)
    class Meta:
        model = LineaParteTrabajo
        fields = ['id', 'parte', 'tarea', 'fecha_inicio', 'fecha_fin', 'finalizada']

class LineaParteTrabajoMovSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaParteTrabajo
        fields = ['id', 'parte', 'tarea', 'fecha_inicio', 'fecha_fin', 'finalizada']

class LineaParteTrabajoNuevaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaParteTrabajo
        fields = ['id', 'parte', 'tarea', 'fecha_inicio', 'fecha_fin', 'finalizada']

class ListadoLineasPartesSerializer(serializers.ModelSerializer):
    parte = ParteTrabajoSerializer(many=False, read_only=True)
    tarea = TareaSerializer(many=False, read_only=True)
    class Meta:
        model = LineaParteTrabajo
        fields = ['id', 'parte', 'tarea', 'fecha_inicio', 'fecha_fin', 'finalizada']