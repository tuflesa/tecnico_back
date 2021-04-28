from rest_framework import serializers
from .models import Empresa, Zona, Seccion, Equipo

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = ['id', 'nombre', 'siglas_zona', 'seccion', 'seccion_nombre', 'fabricante', 'modelo', 'numero', 'imagen', 'zona_id', 'empresa_id']

class ZonaSerializer(serializers.ModelSerializer):
    # secciones = SeccionSerializer(many=True)
    class Meta:
        model = Zona
        fields = ['id','nombre', 'siglas', 'empresa'] #, 'secciones']

class SeccionSerializer(serializers.ModelSerializer):
    # equipos = EquiposSerializer(many=True)
    # zona  = ZonaSerializer(many=False)
    class Meta:
        model = Seccion
        fields = ['id', 'nombre', 'zona', 'siglas_zona', 'empresa_id'] #, 'equipos']

class EstructuraSerializer(serializers.ModelSerializer):
    zonas = ZonaSerializer(many=True)
    class Meta:
        model = Empresa
        fields = ['id', 'nombre', 'siglas', 'zonas']

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'nombre', 'siglas']