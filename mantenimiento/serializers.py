from rest_framework import serializers
from mantenimiento.models import Especialidad, Notificacion, ParteTrabajo, Tarea, TipoPeriodo, TipoTarea
from administracion.serializers import UserSerializer
from estructura.serializers import EquipoSerializer

class NotificacionSerializer(serializers.ModelSerializer):
    quien = UserSerializer(many=False)
    fecha_creacion = serializers.DateField(format="%d-%m-%Y")
    class Meta:
        model = Notificacion
        fields = ['id', 'numero', 'que', 'cuando', 'donde', 'quien', 'como', 'cuanto', 'porque', 'empresa', 'fecha_creacion', 'para', 'revisado', 'descartado', 'finalizado', 'conclusion']

class TareaSerializer(serializers.ModelSerializer):
    #equipo = EquipoSerializer(many=False, read_only=False)
    class Meta:
        model = Tarea
        fields = ['id', 'nombre', 'tipo', 'especialidad', 'tipo_periodo', 'periodo', 'prioridad', 'observaciones', 'tipo_nombre', 'especialidad_nombre', 'pendiente']

class TareaNuevaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id', 'nombre', 'tipo', 'especialidad', 'tipo_periodo', 'periodo', 'prioridad', 'observaciones', 'tipo_nombre', 'especialidad_nombre', 'pendiente']

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
        fields = ['id', 'nombre', 'tipo', 'creada_por', 'observaciones', 'tipo_nombre', 'creado_nombre', 'finalizado', 'fecha_creacion', 'fecha_finalizacion', 'equipo', 'equipo_nombre']

