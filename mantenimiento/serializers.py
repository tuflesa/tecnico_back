from rest_framework import serializers
from mantenimiento.models import Especialidad, Notificacion, Tarea
from administracion.serializers import UserSerializer

class NotificacionSerializer(serializers.ModelSerializer):
    quien = UserSerializer(many=False)
    fecha_creacion = serializers.DateField(format="%d-%m-%Y")
    class Meta:
        model = Notificacion
        fields = ['id', 'numero', 'que', 'cuando', 'donde', 'quien', 'como', 'cuanto', 'porque', 'empresa', 'fecha_creacion', 'para', 'revisado', 'descartado', 'finalizado', 'conclusion']

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id', 'nombre', 'equipo', 'tipo', 'especialidad', 'tipo_periodo', 'periodo', 'prioridad', 'observaciones', 'tipo_nombre', 'equipo_nombre', 'especialidad_nombre']

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ['id', 'nombre']