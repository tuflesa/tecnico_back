from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Aplicacion, Perfil, Puesto, NivelAcceso, DestrezasFoso
from estructura.serializers import EmpresaSerializer, ZonaSerializer, SeccionSerializer
#from mantenimiento.serializers import EspecialidadSerializer
from velocidad.serializers import DestrezasVelocidadSerializer

class AplicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aplicacion
        fields = ['id', 'nombre', 'descripcion', 'imagen', 'url']

class PuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puesto
        fields = ['id', 'nombre']

class NivelAccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelAcceso
        fields = ['id', 'nombre', 'descripcion']

class DestrezasFosoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DestrezasFoso
        fields = ['id', 'nombre', 'descripcion']

class PerfilSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(many=False)
    zona = ZonaSerializer(many=False)
    seccion = SeccionSerializer(many=False) 
    puesto = PuestoSerializer(many=False)
    nivel_acceso = NivelAccesoSerializer(many=False)
    destrezas_velocidad = DestrezasVelocidadSerializer(many=True, read_only=True)
    destrezas_foso      = DestrezasFosoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Perfil
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(many=False, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'get_full_name', 'perfil', 'email']
