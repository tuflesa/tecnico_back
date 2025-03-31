from rest_framework import serializers
from .models import Articulo
from qs.serializers import VarianteSerializer

class ArticuloSerializer(serializers.ModelSerializer):
    variantes = VarianteSerializer(many=True, read_only=False)
    class Meta:
        model = Articulo
        fields = '__all__'