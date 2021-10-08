from django.db.models import fields
from django.db.models.base import Model
from estructura.serializers import EmpresaSerializer, EquipoSerializer
from rest_framework import serializers
from .models import Almacen, Contacto, Inventario, LineaPedido, Movimiento, Pedido, Repuesto, Proveedor, StockMinimo, LineaInventario, TipoRepuesto
from estructura.serializers import EquipoSerializer

class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields='__all__'
        
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProveedorDetailSerializer(serializers.ModelSerializer):
    contactos = ContactoSerializer(many=True, read_only=True)
    class Meta:
        model = Proveedor
        fields = ['id', 'nombre', 'telefono', 'direccion', 'contactos']

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

class PedidoListSerilizer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer(many=False, read_only=True)
    class Meta:
        model = Pedido
        fields = ['id', 'proveedor', 'fecha_creacion', 'fecha_entrega', 'finalizado']

class LineaPedidoSerilizer(serializers.ModelSerializer):
    repuesto = RepuestoListSerializer(many=False, read_only=True)
    class Meta:
        model = LineaPedido
        fields = ['id', 'pedido', 'repuesto', 'cantidad', 'precio']

class PedidoDetailSerilizer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer(many=False, read_only=True)
    lineas_pedido = LineaPedidoSerilizer(many=True, read_only=True)
    class Meta:
        model = Pedido
        fields = ['id', 'proveedor', 'fecha_creacion', 'fecha_entrega', 'finalizado', 'lineas_pedido']