from rest_framework import serializers
from .models import Direcciones, Empresa, Zona, Seccion, Equipo

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = ['id', 'nombre', 'siglas_zona', 'seccion', 'seccion_nombre', 'fabricante', 'modelo', 'numero', 'imagen', 'zona_id', 'empresa_id']

class ZonaSerializer(serializers.ModelSerializer):
    # secciones = SeccionSerializer(many=True)
    class Meta:
        model = Zona
        fields = ['id','nombre', 'siglas', 'empresa', 'empresa_id'] #, 'secciones']

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
        fields = ['id', 'nombre', 'siglas', 'logo','zonas', 'direccion', 'poblacion', 'codpostal', 'telefono', 'cif']

class DireccionesEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direcciones
        fields = ['id', 'empresa', 'direccion', 'codpostal', 'poblacion', 'telefono', 'provincia', 'cif']

class EmpresaSerializer(serializers.ModelSerializer):
    direcciones = DireccionesEmpresaSerializer(many=True)
    class Meta:
        model = Empresa
        fields = ['id', 'nombre', 'siglas', 'direcciones', 'logo', 'direccion', 'poblacion', 'codpostal', 'telefono', 'cif']

class ZonaSerializer_Rodillos(serializers.ModelSerializer): # Lo usamos en la app de rodillos, de ahí su nombre.
    empresa = EmpresaSerializer(many=False)
    class Meta:
        model = Zona
        fields = ['id','nombre', 'siglas', 'empresa', 'empresa_id'] #, 'secciones']

