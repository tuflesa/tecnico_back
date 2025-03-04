from rest_framework import serializers
from .models import Variante

class VarianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variante
        fields = '__all__'