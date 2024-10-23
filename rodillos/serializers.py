from rest_framework import serializers
from estructura.serializers import ZonaSerializer_Rodillos
from administracion.serializers import UserSerializer
from rodillos.models import Rodillo, Plano, Revision, Seccion, Operacion, Tipo_rodillo, Material, Grupo, Tipo_Plano, Nombres_Parametros, Tipo_Seccion, Parametros_Estandar, Eje, Bancada, Conjunto, Elemento, Celda, Forma, Montaje, Icono, Instancia, Rectificacion

class RodilloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rodillo
        fields = ['id', 'nombre', 'operacion', 'grupo', 'tipo', 'tipo_plano', 'diametro', 'forma', 'descripcion_perfil', 'dimension_perfil', 'espesor_1', 'espesor_2', 'espesor', 'num_instancias', 'num_ejes']
class PlanoNuevoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = ['id', 'nombre', 'rodillos', 'cod_antiguo', 'descripcion']

class PlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = ['id', 'nombre', 'rodillos', 'cod_antiguo', 'descripcion']

class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = ['id', 'plano', 'motivo', 'archivo', 'fecha', 'nombre']

class RevisionConjuntosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = ['id', 'plano', 'motivo', 'archivo', 'fecha', 'nombre']

class RevisionPlanosSerializer(serializers.ModelSerializer):
    plano = PlanoSerializer(many=False, read_only=False)
    class Meta:
        model = Revision
        fields = ['id', 'plano', 'motivo', 'archivo', 'fecha', 'nombre']
class SeccionSerializer(serializers.ModelSerializer):
    maquina = ZonaSerializer_Rodillos(many=False, read_only=False)
    class Meta:
        model = Seccion
        fields = ['id', 'nombre', 'maquina', 'pertenece_grupo', 'tipo', 'orden']


class IconoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icono
        fields = ['id', 'nombre', 'icono']

class OperacionSerializer(serializers.ModelSerializer):
    seccion = SeccionSerializer(many=False, read_only=False)
    icono = IconoSerializer(many=False)
    class Meta:
        model = Operacion
        fields = ['id', 'nombre', 'seccion', 'icono', 'orden']

class TipoRodilloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_rodillo
        fields = ['id', 'nombre', 'siglas']
class EjeOperacionSerializer(serializers.ModelSerializer):
    operacion = OperacionSerializer(many=False)
    tipo = TipoRodilloSerializer(many=False)
    class Meta:
        model = Eje
        fields = ['id', 'operacion', 'tipo', 'diametro', 'numero_ejes']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'nombre']

class BancadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bancada
        fields = ['id', 'seccion', 'tubo_madre', 'dimensiones', 'nombre', 'espesores']


class Bancada_GruposSerializer(serializers.ModelSerializer):
    seccion = SeccionSerializer(many=False)
    class Meta:
        model = Bancada
        fields = ['id', 'seccion', 'tubo_madre', 'dimensiones', 'nombre', 'espesores']

class Bancada_CTSerializer(serializers.ModelSerializer):
    seccion = SeccionSerializer(many=False)
    class Meta:
        model = Bancada
        fields = ['id', 'seccion', 'tubo_madre', 'dimensiones', 'nombre', 'espesores']

class GrupoSerializer(serializers.ModelSerializer):
    maquina = ZonaSerializer_Rodillos(many=False, read_only=False)
    bancadas = Bancada_GruposSerializer(many=True, read_only=False)
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'maquina', 'tubo_madre', 'bancadas', 'espesor_1', 'espesor_2']

class GrupoBancadaSerializer(serializers.ModelSerializer):
    maquina = ZonaSerializer_Rodillos(many=False, read_only=False)
    bancadas = Bancada_GruposSerializer(many=True, read_only=False)
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'maquina', 'tubo_madre', 'bancadas', 'espesor_1', 'espesor_2']
    
class Grupo_onlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'maquina', 'tubo_madre', 'bancadas', 'espesor_1', 'espesor_2']

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
    grupo = GrupoSerializer(many=False)
    class Meta:
        model = Rodillo
        fields = ['id', 'nombre', 'operacion', 'grupo', 'tipo', 'tipo_plano', 'diametro', 'forma', 'descripcion_perfil', 'dimension_perfil', 'espesor_1', 'espesor_2', 'espesor', 'num_instancias', 'num_ejes']

class RodillosSerializer(serializers.ModelSerializer):
    grupo = GrupoSerializer(many=False)
    class Meta:
        model = Rodillo
        fields = ['id', 'nombre', 'operacion', 'grupo', 'tipo', 'tipo_plano', 'diametro', 'forma', 'descripcion_perfil', 'dimension_perfil', 'espesor_1', 'espesor_2', 'espesor', 'num_instancias', 'num_ejes']

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
        fields = ['id', 'nombre', 'rodillos', 'cod_antiguo', 'descripcion']

class EjeSerializer(serializers.ModelSerializer):
    tipo = TipoRodilloSerializer(many=False)
    class Meta:
        model = Eje
        fields = ['id', 'operacion', 'tipo', 'diametro', 'numero_ejes']

class Bancada_SelectSerializer(serializers.ModelSerializer):
    seccion = SeccionSerializer()
    class Meta:
        model = Bancada
        fields = ['id', 'seccion', 'tubo_madre', 'dimensiones', 'nombre', 'espesores']

class ConjuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conjunto
        fields = ['id', 'operacion', 'tubo_madre', 'espesores']

class Conjunto_OperacionSerializer(serializers.ModelSerializer):
    operacion = OperacionSerializer()
    class Meta:
        model = Conjunto
        fields = ['id', 'operacion', 'tubo_madre', 'espesores']

class ElementoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elemento
        fields = ['id', 'conjunto', 'eje', 'rodillo', 'anotciones_montaje']

class Conjunto_OperacionSerializer(serializers.ModelSerializer):
    operacion = OperacionSerializer(many=False)
    class Meta:
        model = Conjunto
        fields = ['id', 'operacion', 'tubo_madre', 'espesores']

class Elemento_SelectSerializer(serializers.ModelSerializer):
    conjunto = Conjunto_OperacionSerializer(many=False)
    rodillo = RodilloListSerializer(many=False)
    eje = EjeSerializer(many=False)
    class Meta:
        model = Elemento
        fields = ['id', 'conjunto', 'eje', 'rodillo', 'anotciones_montaje']

class Celda_SelectSerializer(serializers.ModelSerializer):
    conjunto = ConjuntoSerializer(many=False)
    bancada = Bancada_SelectSerializer()
    class Meta:
        model = Celda
        fields = ['id', 'bancada', 'conjunto', 'icono', 'operacion']

class Celda_DuplicarSerializer(serializers.ModelSerializer):
    conjunto = Conjunto_OperacionSerializer(many=False)
    class Meta:
        model = Celda
        fields = ['id', 'bancada', 'conjunto', 'icono', 'operacion']
    
class CeldaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Celda
        fields = ['id', 'bancada', 'conjunto', 'icono', 'operacion']

class FormaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forma
        fields = ['id', 'nombre']

class MontajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Montaje
        fields = ['id', 'nombre', 'maquina', 'grupo', 'bancadas']

class MontajeListadoSerializer(serializers.ModelSerializer):
    maquina = ZonaSerializer_Rodillos(many=False)
    grupo = GrupoSerializer(many=False)
    bancadas = BancadaSerializer(many=False)
    class Meta:
        model = Montaje
        fields = ['id', 'nombre', 'maquina', 'grupo', 'bancadas']

class MontajeToolingSerializer(serializers.ModelSerializer):
    maquina = ZonaSerializer_Rodillos(many=False)
    grupo = GrupoBancadaSerializer(many=False)
    bancadas = BancadaSerializer(many=False)
    class Meta:
        model = Montaje
        fields = ['id', 'nombre', 'maquina', 'grupo', 'bancadas']

class InstanciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instancia
        fields = ['id', 'nombre', 'rodillo', 'material', 'especial', 'diametro', 'diametro_ext', 'activa_qs', 'obsoleta', 'ancho']

class InstanciaListadoSerializer(serializers.ModelSerializer):
    rodillo = RodilloListSerializer(many=False)
    material = MaterialSerializer(many=False)
    class Meta:
        model = Instancia
        fields = ['id', 'nombre', 'rodillo', 'material', 'especial', 'diametro', 'diametro_ext', 'activa_qs', 'obsoleta', 'ancho']

class RectificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rectificacion
        fields = ['id', 'numero', 'creado_por', 'fecha', 'empresa', 'maquina']

class RectificacionListaSerializer(serializers.ModelSerializer):
    maquina = ZonaSerializer_Rodillos(many=False, read_only=False)
    creado_por = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Rectificacion
        fields = ['id', 'numero', 'creado_por', 'fecha', 'empresa', 'maquina']