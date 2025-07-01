from rest_framework import serializers
from estructura.serializers import ZonaSerializer_Rodillos
from administracion.serializers import UserSerializer
from repuestos.serializers import ProveedorSerializer
from articulos.serializers import ArticuloSerializer
from rodillos.models import Rodillo, Plano, Revision, Seccion, Operacion, Tipo_rodillo, Material, Grupo, Tipo_Plano, Nombres_Parametros, Tipo_Seccion, Parametros_Estandar, Eje, Bancada, Conjunto, Elemento, Celda, Forma, Montaje, Icono, Instancia, Rectificacion, LineaRectificacion, Posicion, Icono_celda, Anotaciones

class RodilloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rodillo
        fields = '__all__'

class PlanoNuevoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = '__all__'

class PlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = '__all__'
class RevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = '__all__'

class RevisionConjuntosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revision
        fields = '__all__'

class SeccionSerializer(serializers.ModelSerializer):
    maquina = ZonaSerializer_Rodillos(many=False, read_only=False)
    class Meta:
        model = Seccion
        fields = '__all__'


class IconoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icono
        fields = '__all__'
class Eje_programadoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eje
        fields = '__all__'
class OperacionSerializer(serializers.ModelSerializer):
    posiciones = Eje_programadoresSerializer(many=True)
    seccion = SeccionSerializer(many=False, read_only=False)
    icono = IconoSerializer(many=False)
    class Meta:
        model = Operacion
        fields = '__all__'

class TipoRodilloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_rodillo
        fields = '__all__'
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
        fields = '__all__'

class Bancada_GruposSerializer(serializers.ModelSerializer):
    seccion = SeccionSerializer(many=False)
    class Meta:
        model = Bancada
        fields = '__all__'

class Bancada_CTSerializer(serializers.ModelSerializer):
    seccion = SeccionSerializer(many=False)
    class Meta:
        model = Bancada
        fields = '__all__'

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
        fields = '__all__'

class RodillosSerializer(serializers.ModelSerializer):
    grupo = GrupoSerializer(many=False)
    class Meta:
        model = Rodillo
        fields = '__all__'

class TipoSeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Seccion
        fields = ['id', 'nombre']

class Parametros_estandarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametros_Estandar
        fields = '__all__'

class Plano_existenteSerializer(serializers.ModelSerializer):
    rodillos = RodilloListSerializer(many=True)
    class Meta:
        model = Plano
        fields = ['id', 'nombre', 'rodillos', 'cod_antiguo', 'descripcion', 'xa_rectificado']

class RevisionPlanosSerializer(serializers.ModelSerializer):
    plano = Plano_existenteSerializer(many=False, read_only=False)
    class Meta:
        model = Revision
        fields = ['id', 'plano', 'motivo', 'archivo', 'fecha', 'nombre']

class EjeSerializer(serializers.ModelSerializer):
    tipo = TipoRodilloSerializer(many=False)
    class Meta:
        model = Eje
        fields = ['id', 'operacion', 'tipo', 'diametro', 'numero_ejes']

class Bancada_SelectSerializer(serializers.ModelSerializer):
    seccion = SeccionSerializer()
    class Meta:
        model = Bancada
        fields = '__all__'

class ConjuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conjunto
        fields = '__all__'

class Icono_celdaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icono_celda
        fields = '__all__'

class Conjunto_celdaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Celda
        fields = '__all__'

class Conjunto_OperacionSerializer(serializers.ModelSerializer):
    operacion = OperacionSerializer()
    conjunto_celda = Conjunto_celdaSerializer(many=True, read_only=True)
    class Meta:
        model = Conjunto
        fields = '__all__'

class ElementoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elemento
        fields = ['id', 'conjunto', 'eje', 'rodillo', 'anotciones_montaje']

""" class Conjunto_OperacionSerializer(serializers.ModelSerializer):
    operacion = OperacionSerializer(many=False)
    class Meta:
        model = Conjunto
        fields = '__all__' """

class Elemento_SelectSerializer(serializers.ModelSerializer):
    conjunto = Conjunto_OperacionSerializer(many=False)
    rodillo = RodilloListSerializer(many=False)
    eje = EjeSerializer(many=False)
    class Meta:
        model = Elemento
        fields = ['id', 'conjunto', 'eje', 'rodillo', 'anotciones_montaje']

class Celda_DuplicarSerializer(serializers.ModelSerializer):
    conjunto = Conjunto_OperacionSerializer(many=False)
    class Meta:
        model = Celda
        fields = '__all__'
    
class CeldaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Celda
        fields = '__all__'

class FormaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forma
        fields = ['id', 'nombre']

class MontajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Montaje
        fields = '__all__'

class MontajeListadoSerializer(serializers.ModelSerializer):
    maquina = ZonaSerializer_Rodillos(many=False)
    grupo = GrupoSerializer(many=False)
    bancadas = BancadaSerializer(many=False)
    class Meta:
        model = Montaje
        fields = '__all__'

""" class MontajeToolingSerializer(serializers.ModelSerializer):
    maquina = ZonaSerializer_Rodillos(many=False)
    grupo = GrupoBancadaSerializer(many=False)
    bancadas = BancadaSerializer(many=False)
    class Meta:
        model = Montaje
        fields = ['id', 'nombre', 'maquina', 'grupo', 'bancadas', 'titular_grupo'] """

class InstanciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instancia
        fields = '__all__'

class InstanciaListadoSerializer(serializers.ModelSerializer):
    rodillo = RodilloListSerializer(many=False)
    material = MaterialSerializer(many=False)
    class Meta:
        model = Instancia
        fields = '__all__'

class RectificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rectificacion
        fields = '__all__'

class RectificacionListaSerializer(serializers.ModelSerializer):
    maquina = ZonaSerializer_Rodillos(many=False, read_only=False)
    creado_por = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Rectificacion
        fields = '__all__'

class LineaRectificacionSerializer(serializers.ModelSerializer):
    fecha_rectificado = serializers.DateField(allow_null=True, required=False)
    class Meta:
        model = LineaRectificacion
        fields = '__all__'

""" class LineaRectificacion_toolingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaRectificacion
        fields = '__all__' """
class LineaRectificacion_toolingSerializer(serializers.ModelSerializer): # filtramos aqui que sea finalizado a false
    class Meta:
        model = LineaRectificacion
        fields = '__all__'
    
    def to_representation(self, instance):
        # Aplicar filtrado a nivel de serializador
        if instance.finalizado:
            return None
        return super().to_representation(instance)
    
""" class Instancia_toolingSerializer(serializers.ModelSerializer):
    lineasinstancias = LineaRectificacion_toolingSerializer(many=True)
    class Meta:
        model = Instancia
        fields = '__all__' """

# class PosicionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model: Posicion
#         fields = '__all__'

class Instancia_toolingSerializer(serializers.ModelSerializer):
    lineasinstancias = serializers.SerializerMethodField() 

    class Meta:
        model = Instancia
        fields = '__all__'

    def get_lineasinstancias(self, obj):
        queryset = obj.lineasinstancias.filter(finalizado=False)
        return LineaRectificacion_toolingSerializer(queryset, many=True).data

class PosicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posicion
        fields = '__all__'

class InstanciaQSSerializer(serializers.ModelSerializer):
    #lineasinstancias = serializers.SerializerMethodField() 
    posicion = PosicionSerializer(many=False)
    class Meta:
        model = Instancia
        fields = '__all__'
    
class ListadoLineaRectificacionSerializer(serializers.ModelSerializer):
    fecha_rectificado = serializers.DateField(allow_null=True, required=False)
    rectificado_por = UserSerializer(many=False, read_only=True)
    instancia = InstanciaListadoSerializer(many=False)
    proveedor = ProveedorSerializer(many=False)
    class Meta:
        model = LineaRectificacion
        fields = '__all__'

class OperacionQSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operacion
        fields = '__all__'

class RodilloQSSerializer(serializers.ModelSerializer):
    tipo = TipoRodilloSerializer(many=False)
    instancias = InstanciaQSSerializer(many=True)
    parametros = Parametros_estandarSerializer(many=True)
    tipo_plano = TipoPlanoSerializer(many=False)
    class Meta:
        model = Rodillo
        fields = '__all__'

class ElementoQSSelectSerializer(serializers.ModelSerializer):
    rodillo = RodilloQSSerializer(many=False)
    eje = EjeSerializer(many=False)
    class Meta:
        model = Elemento
        fields = '__all__'

class ConjuntoQSSerializer(serializers.ModelSerializer):
    elementos = ElementoQSSelectSerializer(many=True)
    class Meta:
        model = Conjunto
        fields = '__all__'

class CeldaQSSerializer(serializers.ModelSerializer):
    conjunto = ConjuntoQSSerializer(many=False)
    operacion = OperacionQSSerializer(many = False)
    class Meta:
        model = Celda
        fields = '__all__'

class CeldaToolingSerializer(serializers.ModelSerializer):
    conjunto = ConjuntoQSSerializer(many=False)
    operacion = OperacionQSSerializer(many = False)
    icono = Icono_celdaSerializer(many=False)
    class Meta:
        model = Celda
        fields = '__all__'

class SeccionQSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seccion
        fields = '__all__'

class BancadaQSSerializer(serializers.ModelSerializer):
    seccion = SeccionQSSerializer(many=False)
    celdas = CeldaQSSerializer(many=True)
    class Meta:
        model = Bancada
        fields = '__all__'

class BancadaToolingSerializer(serializers.ModelSerializer):
    seccion = SeccionQSSerializer(many=False)
    celdas = CeldaToolingSerializer(many=True)
    class Meta:
        model = Bancada
        fields = '__all__'

class Celda_SelectSerializer(serializers.ModelSerializer):
    icono = Icono_celdaSerializer(many=False)
    conjunto = ConjuntoSerializer(many=False)
    bancada = BancadaToolingSerializer()
    class Meta:
        model = Celda
        fields = '__all__'
class Operacion_programadoresSerializer(serializers.ModelSerializer):
    posiciones = Eje_programadoresSerializer(many=True, read_only=True)
    class Meta:
        model = Operacion
        fields = '__all__'
        
class Celda_programadoresSerializer(serializers.ModelSerializer):
    icono = Icono_celdaSerializer(many=False)
    conjunto = ConjuntoQSSerializer(many=False)
    operacion = Operacion_programadoresSerializer(many=False)
    bancada = BancadaToolingSerializer()
    class Meta:
        model = Celda
        fields = '__all__'
class GrupoQSSerializer(serializers.ModelSerializer):
    bancadas = BancadaToolingSerializer(many=True)
    class Meta:
        model = Grupo
        fields = ['id', 'nombre', 'maquina', 'tubo_madre', 'bancadas', 'espesor_1', 'espesor_2']

class MontajeQSSerializer(serializers.ModelSerializer):
    grupo = GrupoQSSerializer(many=False)
    bancadas = BancadaQSSerializer(many=False)
    articulos = ArticuloSerializer(many=True)
    class Meta:
        model = Montaje
        fields = '__all__'

class AnotacionesToolingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anotaciones
        fields = '__all__'

class MontajeToolingSerializer(serializers.ModelSerializer):
    grupo = GrupoQSSerializer(many=False)
    bancadas = BancadaToolingSerializer(many=False)
    anotaciones = AnotacionesToolingSerializer(many=True)
    maquina = ZonaSerializer_Rodillos(many=False)
    class Meta:
        model = Montaje
        fields = '__all__'
    
class AnotacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anotaciones
        fields = '__all__'