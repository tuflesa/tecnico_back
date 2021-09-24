from django.db.models import fields
from django.db.models.base import Model
from estructura.serializers import EmpresaSerializer, EquipoSerializer
from rest_framework import serializers
from .models import Almacen, Contacto, Inventario, Movimiento, Repuesto, Proveedor, StockMinimo, LineaInventario, TipoRepuesto
from estructura.serializers import EquipoSerializer

class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        Model = Contacto
        fields='__all__'
        
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class AlmacenSerilizer(serializers.ModelSerializer):
    # empresa = EmpresaSerializer(many=False, read_only=False)
    class Meta:
        model = Almacen
        fields = ['id', 'nombre', 'empresa', 'empresa_siglas']

class StockMinimoSerializer(serializers.ModelSerializer):
    # almacen = AlmacenSerilizer(many=False, read_only=True)
    class Meta:
        model = StockMinimo
        fields = ['id', 'repuesto', 'almacen', 'cantidad']

class RepuestoDetailSerializer(serializers.ModelSerializer):
    equipos = EquipoSerializer(many=True, read_only=True)
    proveedores = ProveedorSerializer(many=True, read_only=True)
    stocks_minimos = StockMinimoSerializer(many=True, read_only=True)
    class Meta:
        model = Repuesto
        fields = ['id', 'nombre', 'tipo_repuesto', 'fabricante', 'modelo', 'stock', 'es_critico', 'equipos', 'proveedores', 'stocks_minimos', 'descatalogado']

class RepuestoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repuesto
        fields = ['id', 'nombre', 'tipo_repuesto','fabricante', 'modelo', 'es_critico', 'descatalogado', 'equipos', 'proveedores']

class TipoRepuestoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = TipoRepuesto
        fields = ['id', 'nombre'] 

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = ['id', 'nombre', 'fecha_creacion', 'responsable']

class LineaInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaInventario
        fields = ['id', 'inventario', 'repuesto', 'almacen', 'cantidad']

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = ['id', 'fecha', 'cantidad', 'almacen', 'usuario', 'linea_pedido', 'linea_inventario']