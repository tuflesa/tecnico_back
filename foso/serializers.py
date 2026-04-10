from rest_framework import serializers
from .models import (
    Foso, Linea, Posicion, Bobina, Ocupacion, Material, Proveedor
)


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = "__all__"


class FosoSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(
        source='empresa.nombre',
        read_only=True
    )

    class Meta:
        model = Foso
        fields = [
            "id",
            "empresa",
            "empresa_nombre",
            "nombre",
            "descripcion",
            "activo",
            "columnas_por_altura",
        ]


class LineaSerializer(serializers.ModelSerializer):
    foso_nombre = serializers.CharField(
        source='foso.nombre',
        read_only=True
    )
    empresa_nombre = serializers.CharField(
        source='foso.empresa.nombre',
        read_only=True
    )

    class Meta:
        model = Linea
        fields = [
            "id",
            "foso",
            "foso_nombre",
            "empresa_nombre",
            "nombre",
            "descripcion",
            "activa",
        ]


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
        if not pos:
            return None

        return {
            "id":           pos.id,
            "linea_id":     pos.linea.id,
            "linea_nombre": pos.linea.nombre,
            "foso_id":      pos.linea.foso.id,
            "foso_nombre":  pos.linea.foso.nombre,
            "altura":       pos.altura,
            "columna":      pos.columna,
        }


class OcupacionSerializer(serializers.ModelSerializer):
    bobina_detalle   = BobinaSerializer(source="bobina", read_only=True)
    posicion_detalle = serializers.SerializerMethodField()

    class Meta:
        model = Ocupacion
        fields = "__all__"

    def get_posicion_detalle(self, obj):
        return {
            "id": obj.posicion.id,
            "linea_id": obj.posicion.linea.id,
            "foso_id": obj.posicion.linea.foso.id,
            "altura": obj.posicion.altura,
            "columna": obj.posicion.columna,
        }


class PosicionSerializer(serializers.ModelSerializer):
    ocupacion_activa = serializers.SerializerMethodField()
    max_columnas = serializers.ReadOnlyField()

    class Meta:
        model = Posicion
        fields = [
            "id",
            "linea",
            "altura",
            "columna",
            "habilitada",
            "max_columnas",
            "ocupacion_activa",
        ]

    def get_ocupacion_activa(self, obj):
        oc = obj.ocupacion_activa
        if not oc:
            return None

        return {
            "ocupacion_id": oc.id,
            "bobina_id": oc.bobina.id,
            "bobina_codigo": oc.bobina.codigo,
            "fecha_inicio": oc.fecha_inicio,
        }


class FosoLineaSerializer(serializers.ModelSerializer):
    """
    Devuelve UNA línea con su grid completo.
    La geometría se obtiene SIEMPRE del foso.
    """
    alturas = serializers.SerializerMethodField()

    class Meta:
        model = Linea
        fields = [
            "id",
            "nombre",
            "descripcion",
            "activa",
            "alturas",
        ]

    def get_alturas(self, linea):
        """
        Construye el grid a partir de:
        - foso.columnas_por_altura
        - posiciones reales existentes
        """
        columnas_por_altura = linea.foso.columnas_por_altura

        # Indexamos posiciones por (altura, columna)
        posiciones = {
            (p.altura, p.columna): p
            for p in linea.posiciones
                         .select_related()
                         .prefetch_related("ocupaciones__bobina")
                         .all()
        }

        resultado = []

        # IMPORTANTE: ordenar las alturas
        alturas_ordenadas = sorted(
            int(k) for k in columnas_por_altura.keys()
        )

        for altura in alturas_ordenadas:
            max_col = columnas_por_altura[str(altura)]
            columnas = []

            for col in range(1, max_col + 1):
                pos = posiciones.get((altura, col))

                celda = {
                    "columna": col,
                    "posicion_id": pos.id if pos else None,
                    "habilitada": pos.habilitada if pos else True,
                }

                if pos:
                    oc = pos.ocupacion_activa
                    if oc:
                        celda["bobina_id"] = oc.bobina.id
                        celda["bobina_codigo"] = oc.bobina.codigo

                columnas.append(celda)
            resultado.append({"altura": altura, "columnas": columnas})

        return resultado


class ColocarBobinaSerializer(serializers.Serializer):
    bobina_id = serializers.IntegerField()
    posicion_id = serializers.IntegerField()
    notas = serializers.CharField(
        required=False,
        allow_blank=True
    )

    def validate_bobina_id(self, value):
        if not Bobina.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Bobina no encontrada.")
        return value

    def validate_posicion_id(self, value):
        if not Posicion.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Posición no encontrada.")
        return value
