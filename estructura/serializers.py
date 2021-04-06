from rest_framework import serializers
from .models import Empresa, Zona, Seccion, Equipo

class EquiposSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'

class SeccionSerializer(serializers.ModelSerializer):
    equipos = EquiposSerializer(many=True)
    class Meta:
        model = Seccion
        fields = ['nombre', 'equipos']

class ZonaSerializer(serializers.ModelSerializer):
    secciones = SeccionSerializer(many=True)
    class Meta:
        model = Zona
        fields = ['nombre', 'siglas', 'secciones']

class EmpresaSerializer(serializers.ModelSerializer):
    zonas = ZonaSerializer(many=True)
    class Meta:
        model = Empresa
        fields = ['id', 'nombre', 'siglas', 'zonas']