from rest_framework import serializers
from estructura.serializers import ZonaSerializer_Rodillos
from rodillos.models import Rodillo, Plano, Revision, Seccion, Operacion, Tipo_rodillo, Material, Grupo, Tipo_Plano, Nombres_Parametros, Tipo_Seccion, Parametros_Estandar, Eje, Bancada, Conjunto, Elemento, Celda, Forma

class RodilloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rodillo
        fields = ['id', 'nombre', 'operacion', 'grupo', 'tipo', 'material', 'tipo_plano', 'diametro', 'forma', 'descripcion_perfil', 'dimension_perfil']
class PlanoNuevoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = ['id', 'nombre', 'rodillos']

class PlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = ['id', 'nombre', 'rodillos']

class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = ['id', 'plano', 'motivo', 'archivo', 'fecha']

class RevisionConjuntosSerializer(serializers.ModelSerializer):
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

class BancadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bancada
        fields = ['id', 'seccion', 'tubo_madre', 'dimensiones', 'nombre']


class Bancada_GruposSerializer(serializers.ModelSerializer):
    seccion = SeccionSerializer(many=False)
    class Meta:
        model = Bancada
        fields = ['id', 'seccion', 'tubo_madre', 'dimensiones', 'nombre']

class GrupoSerializer(serializers.ModelSerializer):
    maquina = ZonaSerializer_Rodillos(many=False, read_only=False)
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'maquina', 'tubo_madre', 'bancadas']
    
class Grupo_onlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'maquina', 'tubo_madre', 'bancadas']

class TipoPlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Plano
        fields = ['id', 'nombre', 'tipo_seccion', 'croquis', 'nombres', 'tipo_rodillo']

class Nombres_ParametrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nombres_Parametros
        fields = ['id', 'nombre', 'descripcion']

class PlanoParametrosSerializer(serializers.ModelSerializer):
    nombres = Nombres_ParametrosSerializer(many=True, read_only=False)
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
        fields = ['id', 'nombre', 'operacion', 'grupo', 'tipo', 'material', 'tipo_plano', 'diametro', 'forma', 'descripcion_perfil', 'dimension_perfil']

class TipoSeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Seccion
        fields = ['id', 'nombre']

class Parametros_estandarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametros_Estandar
        fields = ['id', 'nombre', 'valor', 'rodillo']

class Plano_existenteSerializer(serializers.ModelSerializer):
    rodillos = RodilloListSerializer(many=True)
    class Meta:
        model = Plano
        fields = ['id', 'nombre', 'rodillos']

class EjeSerializer(serializers.ModelSerializer):
    tipo = TipoRodilloSerializer(many=False)
    class Meta:
        model = Eje
        fields = ['id', 'operacion', 'tipo', 'diametro']

class Bancada_SelectSerializer(serializers.ModelSerializer):
    seccion = SeccionSerializer()
    class Meta:
        model = Bancada
        fields = ['id', 'seccion', 'tubo_madre', 'dimensiones', 'nombre']

class ConjuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conjunto
        fields = ['id', 'operacion', 'tubo_madre']

class ElementoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elemento
        fields = ['id', 'conjunto', 'eje', 'rodillo']

class Conjunto_OperacionSerializer(serializers.ModelSerializer):
    operacion = OperacionSerializer(many=False)
    class Meta:
        model = Conjunto
        fields = ['id', 'operacion', 'tubo_madre']

class Elemento_SelectSerializer(serializers.ModelSerializer):
    conjunto = Conjunto_OperacionSerializer(many=False)
    rodillo = RodilloListSerializer(many=False)
    eje = EjeSerializer(many=False)
    class Meta:
        model = Elemento
        fields = ['id', 'conjunto', 'eje', 'rodillo']

class Celda_SelectSerializer(serializers.ModelSerializer):
    conjunto = ConjuntoSerializer(many=False)
    bancada = Bancada_SelectSerializer()
    class Meta:
        model = Celda
        fields = ['id', 'bancada', 'conjunto', 'icono']
    
class CeldaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Celda
        fields = ['id', 'bancada', 'conjunto', 'icono']

class FormaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forma
        fields = ['id', 'nombre']
