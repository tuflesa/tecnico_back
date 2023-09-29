from rest_framework import serializers
from estructura.serializers import ZonaSerializer_Rodillos
from rodillos.models import Rodillo, Plano, Revision, Seccion, Operacion, Tipo_rodillo, Material, Grupo, Tipo_Plano, Nombres_Parametros, Tipo_Seccion

class RodilloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rodillo
        fields = ['id', 'nombre', 'operacion', 'grupo', 'tipo', 'material', 'tipo_plano']
class PlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = ['id', 'nombre', 'rodillos']

class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = ['id', 'plano', 'motivo', 'archivo', 'fecha']

class SeccionSerializer(serializers.ModelSerializer):
    maquina = ZonaSerializer_Rodillos(many=False, read_only=False)
    class Meta:
        model = Seccion
        fields = ['id', 'nombre', 'maquina', 'pertenece_grupo', 'tipo']

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
        fields = ['id', 'nombre', 'tipo_seccion', 'croquis', 'nombres', 'tipo_rodillo']

class ParametrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nombres_Parametros
        fields = ['id', 'nombre', 'descripcion']

class PlanoParametrosSerializer(serializers.ModelSerializer):
    nombres = ParametrosSerializer(many=True, read_only=False)
    class Meta:
        model = Tipo_Plano
        fields = ['id', 'nombre', 'tipo_seccion', 'croquis', 'nombres', 'tipo_rodillo']

class RodilloListSerializer(serializers.ModelSerializer):
    operacion = OperacionSerializer(many=False, read_only=False)
    tipo = TipoRodilloSerializer(many=False)
    material = MaterialSerializer(many=False)
    grupo = GrupoSerializer(many=False)
    class Meta:
        model = Rodillo
        fields = ['id', 'nombre', 'operacion', 'grupo', 'tipo', 'material', 'tipo_plano']

class TipoSeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Seccion
        fields = ['id', 'nombre']

