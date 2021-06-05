from rest_framework import serializers
from .models import ZonaPerfilVelocidad, Registro
from estructura.serializers import ZonaSerializer

class ZonaPerfilVelocidadSerilizer(serializers.ModelSerializer):
    zona = ZonaSerializer(many=False)
    class Meta:
        model = ZonaPerfilVelocidad
        fields = ['id', 'zona', 'ip', 'rack', 'slot', 'db', 'dw', 'color']

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = ['id', 'fecha', 'hora', 'zona', 'velocidad']