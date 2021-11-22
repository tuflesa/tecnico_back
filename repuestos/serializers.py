from django.db.models import fields
from django.db.models.base import Model
from estructura.serializers import EmpresaSerializer, EquipoSerializer
from rest_framework import serializers
from .models import Entrega, LineaAdicional, Almacen, Contacto, Inventario, LineaPedido, Movimiento, Pedido, Repuesto, Proveedor, StockMinimo, LineaInventario, TipoRepuesto
from estructura.serializers import EquipoSerializer
from estructura.serializers import EstructuraSerializer
from administracion.serializers import UserSerializer

class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields='__all__'
        
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProveedorRepuSerializer(serializers.ModelSerializer):
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
        fields = ['id', 'nombre', 'empresa', 'empresa_siglas', 'empresa_id']

class StockMinimoSerializer(serializers.ModelSerializer):
    #almacen = AlmacenSerilizer(many=False, read_only=True)
    class Meta:
        model = StockMinimo
        fields = ['id', 'repuesto', 'almacen', 'cantidad', 'localizacion', 'stock_act']

class StockMinimoDetailSerializer(serializers.ModelSerializer):
    almacen = AlmacenSerilizer(many=False, read_only=True)
    class Meta:
        model = StockMinimo
        fields = ['id', 'repuesto', 'almacen', 'cantidad', 'localizacion', 'stock_act']

class RepuestoDetailSerializer(serializers.ModelSerializer):
    equipos = EquipoSerializer(many=True, read_only=True)
    proveedores = ProveedorSerializer(many=True, read_only=True)
    stocks_minimos = StockMinimoDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Repuesto
        fields = ['id', 'nombre', 'tipo_repuesto', 'fabricante', 'modelo', 'es_critico', 'equipos', 'proveedores', 'stocks_minimos', 'descatalogado']

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
        fields = ['id', 'fecha', 'cantidad', 'almacen', 'usuario', 'linea_pedido', 'linea_inventario', 'albaran']

class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = ['id', 'fecha', 'cantidad', 'usuario', 'linea_adicional', 'albaran']

class MovimientoDetailSerializer(serializers.ModelSerializer):
    almacen = AlmacenSerilizer(many=False, read_only=True)
    class Meta:
        model = Movimiento
        fields = ['id', 'fecha', 'cantidad', 'almacen', 'usuario', 'linea_pedido', 'linea_inventario', 'albaran']        

class PedidoListSerilizer(serializers.ModelSerializer):
    empresa = EstructuraSerializer(many=False, read_only=True)
    proveedor = ProveedorSerializer(many=False, read_only=True)
    class Meta:
        model = Pedido
        fields = ['id','proveedor','empresa', 'numero', 'fecha_creacion', 'fecha_entrega', 'finalizado', 'creado_por']

class LineaPedidoDetailSerilizer(serializers.ModelSerializer):
    repuesto = RepuestoListSerializer(many=False, read_only=True)
    class Meta:
        model = LineaPedido
        fields = ['id', 'por_recibir', 'pedido', 'repuesto', 'cantidad', 'precio']

class LineaPedidoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = LineaPedido
        fields = ['id', 'pedido', 'por_recibir' ,'repuesto', 'cantidad', 'precio']

class LineasAdicionalesSerilizer(serializers.ModelSerializer):
    class Meta:
        model = LineaAdicional
        fields = ['id', 'pedido', 'descripcion', 'cantidad', 'precio', 'por_recibir']

class PedidoDetailSerilizer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer(many=False, read_only=True)
    lineas_pedido = LineaPedidoDetailSerilizer(many=True, read_only=True)
    lineas_adicionales = LineasAdicionalesSerilizer(many=True, read_only=True)
    creado_por = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Pedido
        fields = ['id', 'proveedor', 'empresa', 'numero', 'fecha_creacion', 'fecha_entrega', 'finalizado', 'lineas_pedido', 'creado_por', 'lineas_adicionales']

class PedidoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['id', 'proveedor','empresa', 'numero', 'fecha_creacion', 'fecha_entrega', 'finalizado', 'creado_por']