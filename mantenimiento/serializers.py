from rest_framework import serializers
from mantenimiento.models import Notificacion
from administracion.serializers import UserSerializer

class NotificacionSerializer(serializers.ModelSerializer):
    quien = UserSerializer(many=False)
    fecha_creacion = serializers.DateField(format="%d-%m-%Y")
    class Meta:
        model = Notificacion
        fields = ['id', 'numero', 'que', 'cuando', 'donde', 'quien', 'como', 'cuanto', 'porque', 'empresa', 'fecha_creacion', 'para', 'revisado', 'descartado', 'finalizado', 'conclusion']