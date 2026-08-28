from rest_framework import serializers
from .models import Articulo, Calidad, Acabado, Norma, Formas
from qs.serializers import VarianteSerializer

class ArticuloSerializer(serializers.ModelSerializer):
    variantes = VarianteSerializer(many=True, read_only=True)
    class Meta:
        model = Articulo
        fields = '__all__'

class FormasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formas
        fields = '__all__'
 
 
class CalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calidad
        fields = '__all__'
 
 
class AcabadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acabado
        fields = '__all__'
 
 
class NormaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Norma
        fields = '__all__'