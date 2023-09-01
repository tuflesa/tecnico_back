from rest_framework import serializers
from estructura.serializers import ZonaSerializer
from rodillos.models import Rodillo, Plano, Revision, Seccion, Operacion, Tipo_rodillo, Material, Grupo, Tipo_Plano

class RodilloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rodillo
        fields = ['id', 'nombre', 'operacion', 'grupo', 'tipo', 'material']
class PlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = ['id', 'nombre', 'rodillos']

class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = ['id', 'plano', 'motivo', 'archivo', 'fecha']

class SeccionSerializer(serializers.ModelSerializer):
    maquina = ZonaSerializer(many=False, read_only=False)
    class Meta:
        model = Seccion
        fields = ['id', 'nombre', 'maquina', 'pertenece_grupo']

class OperacionSerializer(serializers.ModelSerializer):
    seccion = SeccionSerializer(many=False, read_only=False)
    class Meta:
        model = Operacion
        fields = ['id', 'nombre', 'seccion', 'icono']

class TipoRodilloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_rodillo
        fields = ['id', 'nombre']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'nombre']

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'maquina', 'tubo_madre']

class TipoPlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Plano
        fields = ['id', 'nombre', 'tipo_seccion', 'croquis', 'nombres']

class RodilloListSerializer(serializers.ModelSerializer):
    operacion = OperacionSerializer(many=False, read_only=False)
    tipo = TipoRodilloSerializer(many=False)
    material = MaterialSerializer(many=False)
    grupo = GrupoSerializer(many=False)
    class Meta:
        model = Rodillo
        fields = ['id', 'nombre', 'operacion', 'grupo', 'tipo', 'material']

