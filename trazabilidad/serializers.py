from rest_framework import serializers
from .models import Acumulador, Flejes, Tubos
from estructura.serializers import ZonaSerializer

class AcumuladorSerializer(serializers.ModelSerializer):
    zona = ZonaSerializer(many=False)
    class Meta:
        model = Acumulador
        fields = '__all__'

class TubosSerializer(serializers.ModelSerializer):
    descripcion = serializers.SerializerMethodField()
    class Meta:
        model = Tubos
        fields = '__all__'
    def get_descripcion(self, obj):
        return obj.descripcion()

class FlejesSerializer(serializers.ModelSerializer):
    tubos = TubosSerializer(many=True)
    class Meta:
        model = Flejes
        fields = ['pos', 'idProduccion', 'IdArticulo', 'peso', 'of', 'maquina_siglas', 'descripcion', 'acumulador', 'ancho', 'espesor', 'metros_teorico', 'metros_medido', 'metros_tubo', 'tubos', 'metros_salida']

class FlejesSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flejes
        fields = '__all__'

