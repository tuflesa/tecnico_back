from rest_framework import serializers
from rodillos.models import Seccion, Operacion, Posicion, Conjunto, Elemento, Rodillo, Montaje, Grupo, Ficheros, Material
from administracion.serializers import UserSerializer
from estructura.serializers import EquipoSerializer, SeccionSerializer, ZonaSerializer

class ConjuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conjunto
        fields = ['id', 'nombre', 'elementos', 'tubo_madre']

class GruposSerializer(serializers.ModelSerializer):
    conjuntos = ConjuntoSerializer(many=True, read_only=True)
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'conjuntos', 'tubo_madre', 'maquina']


