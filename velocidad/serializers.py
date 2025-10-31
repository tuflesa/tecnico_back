from rest_framework import serializers
from .models import ZonaPerfilVelocidad, Registro
from estructura.serializers import ZonaSerializer

class ZonaPerfilVelocidadSerilizer(serializers.ModelSerializer):
    zona = ZonaSerializer(many=False)
    class Meta:
        model = ZonaPerfilVelocidad
        fields = ['id', 'zona', 'ip', 'rack', 'slot', 'db', 'dw', 'nwords', 'color', 'v_max', 'hf_pmax', 'hf_fmax', 'hf_fmin', 'fuerza_max']

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = ['id', 'fecha', 'hora', 'zona', 'velocidad', 'potencia', 'frecuencia', 'presion']