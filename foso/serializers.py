from rest_framework import serializers
from .models import Linea, Posicion, Bobina, Ocupacion, Material, Proveedor, COLUMNAS_POR_ALTURA

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Material
        fields = "__all__"

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Proveedor
        fields = "__all__"
class LineaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Linea
        fields = "__all__"


class BobinaSerializer(serializers.ModelSerializer):
    en_foso          = serializers.ReadOnlyField()
    posicion_actual  = serializers.SerializerMethodField()
    material_nombre  = serializers.CharField(source='material.nombre',  read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)

    class Meta:
        model = Bobina
        fields = "__all__"

    def get_posicion_actual(self, obj):
        pos = obj.posicion_actual
        if pos:
            return {
                "id": pos.id,
                "linea": pos.linea.id,
                "linea_nombre": pos.linea.nombre,
                "altura": pos.altura,
                "columna": pos.columna,
            }
        return None


class OcupacionSerializer(serializers.ModelSerializer):
    bobina_detalle = BobinaSerializer(source="bobina", read_only=True)
    posicion_detalle = serializers.SerializerMethodField()

    class Meta:
        model = Ocupacion
        fields = "__all__"

    def get_posicion_detalle(self, obj):
        return {
            'id':      obj.posicion.id,
            'linea':   obj.posicion.linea.id,
            'altura':  obj.posicion.altura,
            'columna': obj.posicion.columna,
        }


class PosicionSerializer(serializers.ModelSerializer):
    """Posición con su ocupación activa (si la hay)."""
    ocupacion_activa = serializers.SerializerMethodField()
    max_columnas     = serializers.ReadOnlyField()

    class Meta:
        model = Posicion
        fields = ["id", "linea", "altura", "columna", "max_columnas", "ocupacion_activa"]

    def get_ocupacion_activa(self, obj):
        oc = obj.ocupacion_activa
        if oc:
            return {
                "ocupacion_id": oc.id,
                "bobina_id":    oc.bobina.id,
                "bobina_codigo": oc.bobina.codigo,
                "fecha_inicio": oc.fecha_inicio,
            }
        return None


# ─── Serializer especial: mapa completo del foso ───────────────────────────
class FosoLineaSerializer(serializers.ModelSerializer):
    """
    Devuelve una línea con su grid completo.
    Estructura: { linea, alturas: [ { altura, columnas: [ {col, posicion_id, bobina?} ] } ] }
    """
    alturas = serializers.SerializerMethodField()

    class Meta:
        model = Linea
        fields = ["id", "nombre", "descripcion", "activa", "alturas"]

    def get_alturas(self, linea):
        posiciones = {
            (p.altura, p.columna): p
            for p in linea.posiciones.prefetch_related(
                "ocupaciones__bobina"
            ).all()
        }

        resultado = []
        for altura, max_col in COLUMNAS_POR_ALTURA.items():
            columnas = []
            for col in range(1, max_col + 1):
                pos = posiciones.get((altura, col))
                celda = {"columna": col, "posicion_id": pos.id if pos else None, "habilitada": pos.habilitada if pos else True}
                if pos:
                    oc = pos.ocupacion_activa
                    if oc:
                        celda["bobina_id"]    = oc.bobina.id
                        celda["bobina_codigo"] = oc.bobina.codigo
                columnas.append(celda)
            resultado.append({"altura": altura, "columnas": columnas})

        return resultado


# ─── Serializer para colocar/mover bobina ──────────────────────────────────
class ColocarBobinaSerializer(serializers.Serializer):
    bobina_id   = serializers.IntegerField()
    posicion_id = serializers.IntegerField()
    notas       = serializers.CharField(required=False, allow_blank=True)

    def validate_bobina_id(self, value):
        if not Bobina.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Bobina no encontrada.")
        return value

    def validate_posicion_id(self, value):
        if not Posicion.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Posición no encontrada.")
        return value