from rest_framework import serializers
from .models import Acumulador, Flejes
from estructura.serializers import ZonaSerializer

class AcumuladorSerializer(serializers.ModelSerializer):
    zona = ZonaSerializer(many=False)
    class Meta:
        model = Acumulador
        fields = '__all__'

class FlejesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flejes
        fields = ['pos', 'idProduccion', 'IdArticulo', 'peso', 'of', 'maquina_siglas', 'descripcion', 'acumulador', 'ancho', 'espesor', 'metros_teorico']