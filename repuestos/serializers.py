from django.db.models import fields
from django.db.models.base import Model
from estructura.serializers import DireccionesEmpresaSerializer, EmpresaSerializer, EquipoSerializer
from rest_framework import serializers
from .models import PrecioRepuesto, Entrega, LineaAdicional, Almacen, Contacto, Inventario, LineaPedido, LineaSalida, Movimiento, Pedido, Repuesto, Proveedor, Salida, StockMinimo, LineaInventario, TipoRepuesto, TipoUnidad
from estructura.serializers import EquipoSerializer
from estructura.serializers import EstructuraSerializer
from estructura.serializers import EmpresaSerializer
from administracion.serializers import UserSerializer

class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields='__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class TipoUnidadSerilizer(serializers.ModelSerializer):
    class Meta:
        model = TipoUnidad
        fields = ['id', 'nombre', 'siglas'] 

class ProveedorRepuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProveedorDetailSerializer(serializers.ModelSerializer):
    contactos = ContactoSerializer(many=True, read_only=True)
    class Meta:
        model = Proveedor
        fields = ['id', 'nombre', 'telefono', 'direccion', 'contactos', 'condicion_pago', 'condicion_entrega', 'poblacion', 'cif', 'pais', 'cod_ekon', 'de_rectificado']

class AlmacenSerilizer(serializers.ModelSerializer):
    # empresa = EmpresaSerializer(many=False, read_only=False)
    class Meta:
        model = Almacen
        fields = ['id', 'nombre', 'empresa', 'empresa_siglas', 'empresa_id']

class RepuestoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repuesto
        fields = ['id', 'nombre', 'unidad_nombre', 'unidad_siglas', 'tipo_repuesto', 'tipo_unidad','fabricante', 'modelo', 'es_critico', 'descatalogado', 'equipos', 'proveedores', 'observaciones', 'nombre_comun']

class StockMinimoSerializer(serializers.ModelSerializer):
    #almacen = AlmacenSerilizer(many=False, read_only=True)
    class Meta:
        model = StockMinimo
        fields = '__all__'

class StockMinimoDetailSerializer(serializers.ModelSerializer):
    almacen = AlmacenSerilizer(many=False, read_only=True)
    repuesto = RepuestoListSerializer(many=False, read_only=True)
    class Meta:
        model = StockMinimo
        fields = '__all__'

class RepuestoDetailSerializer(serializers.ModelSerializer):
    equipos = EquipoSerializer(many=True, read_only=True)
    proveedores = ProveedorSerializer(many=True, read_only=True)
    stocks_minimos = StockMinimoDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Repuesto
        fields = ['id', 'nombre', 'tipo_repuesto', 'tipo_unidad', 'fabricante', 'modelo', 'es_critico', 'equipos', 'proveedores', 'stocks_minimos', 'descatalogado', 'observaciones', 'nombre_comun']

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

class LineaInventarioTrazaSerializer(serializers.ModelSerializer):
    inventario = InventarioSerializer(many=False, read_only=True)
    class Meta:
        model = LineaInventario
        fields = ['id', 'inventario', 'repuesto', 'almacen', 'cantidad']

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = ['id', 'fecha', 'cantidad', 'almacen', 'usuario', 'linea_pedido', 'linea_inventario', 'linea_salida', 'albaran']

class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = ['id', 'fecha', 'cantidad', 'usuario', 'linea_adicional', 'albaran']

class MovimientoDetailSerializer(serializers.ModelSerializer):
    almacen = AlmacenSerilizer(many=False, read_only=True)
    class Meta:
        model = Movimiento
        fields = ['id', 'fecha', 'cantidad', 'almacen', 'usuario', 'linea_pedido', 'linea_inventario', 'linea_salida', 'albaran']        

class PedidoListSerilizer(serializers.ModelSerializer):
    empresa = EstructuraSerializer(many=False, read_only=True)
    proveedor = ProveedorSerializer(many=False, read_only=True)
    creado_por = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Pedido
        fields = ['id','proveedor','empresa', 'numero', 'fecha_creacion', 'fecha_entrega', 'fecha_prevista_entrega', 'finalizado', 'creado_por', 'direccion_envio', 'contacto', 'observaciones', 'observaciones2', 'descripcion', 'intervencion', 'revisado']

class LineaPedidoDetailSerilizer(serializers.ModelSerializer):
    repuesto = RepuestoListSerializer(many=False, read_only=True)    
    class Meta:
        model = LineaPedido
        fields = ['id', 'por_recibir', 'pedido', 'repuesto', 'cantidad', 'precio', 'descuento', 'total', 'descripcion_proveedor', 'modelo_proveedor']

class LineaPedidoTrazaSerilizer(serializers.ModelSerializer):
    repuesto = RepuestoListSerializer(many=False, read_only=True)    
    pedido = PedidoListSerilizer(many=False, read_only=True)
    class Meta:
        model = LineaPedido
        fields = ['id', 'por_recibir', 'pedido', 'repuesto', 'cantidad', 'precio', 'descuento', 'total', 'descripcion_proveedor', 'modelo_proveedor']

class LineaPedidoSerilizer(serializers.ModelSerializer):
    #pedido = PedidoListSerilizer(many=False, read_only=True)
    class Meta:
        model = LineaPedido
        fields = ['id', 'pedido', 'por_recibir' ,'repuesto', 'cantidad', 'precio', 'descuento', 'total', 'descripcion_proveedor', 'modelo_proveedor']

class LineaPedidoPendSerilizer(serializers.ModelSerializer):
    repuesto = RepuestoListSerializer(many=False, read_only=True) 
    pedido = PedidoListSerilizer(many=False, read_only=True)
    class Meta:
        model = LineaPedido
        fields = ['id', 'pedido', 'por_recibir' ,'repuesto', 'cantidad', 'precio', 'descuento', 'total', 'descripcion_proveedor', 'modelo_proveedor']

class LineasAdicionalesSerilizer(serializers.ModelSerializer):
    class Meta:
        model = LineaAdicional
        fields = ['id', 'pedido', 'descripcion', 'cantidad', 'precio', 'por_recibir', 'descuento', 'total']

class LineasAdicionalesDetalleSerilizer(serializers.ModelSerializer):
    pedido = PedidoListSerilizer(many=False, read_only=True)
    class Meta:
        model = LineaAdicional
        fields = ['id', 'pedido', 'descripcion', 'cantidad', 'precio', 'por_recibir', 'descuento', 'total']

class PedidoDetailSerilizer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer(many=False, read_only=True)
    lineas_pedido = LineaPedidoDetailSerilizer(many=True, read_only=True)
    lineas_adicionales = LineasAdicionalesSerilizer(many=True, read_only=True)
    creado_por = UserSerializer(many=False, read_only=True)
    contacto = ContactoSerializer(many=False)
    direccion_envio = DireccionesEmpresaSerializer(many=False)
    empresa = EmpresaSerializer(many=False)
    class Meta:
        model = Pedido
        fields = ['id', 'proveedor', 'empresa', 'numero', 'fecha_creacion', 'fecha_entrega', 'fecha_prevista_entrega', 'finalizado', 'contacto', 'direccion_envio', 'lineas_pedido', 'creado_por', 'lineas_adicionales', 'observaciones', 'observaciones2', 'descripcion', 'intervencion', 'revisado']

class PedidoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['id', 'proveedor','empresa', 'numero', 'fecha_creacion', 'fecha_entrega', 'fecha_prevista_entrega', 'finalizado', 'creado_por','contacto','direccion_envio', 'observaciones', 'observaciones2', 'descripcion', 'intervencion', 'revisado']

class SalidasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salida
        fields = ['id', 'nombre', 'fecha_creacion', 'responsable']

class LineaSalidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaSalida
        fields = ['id', 'salida', 'repuesto', 'almacen', 'cantidad']


class LineaSalidaTrazaSerializer(serializers.ModelSerializer):
    salida = SalidasSerializer(many=False, read_only=True)
    class Meta:
        model = LineaSalida
        fields = ['id', 'salida', 'repuesto', 'almacen', 'cantidad']

class MovimientoTrazabilidadSerializer(serializers.ModelSerializer):
    almacen = AlmacenSerilizer(many=False, read_only=True)
    linea_salida = LineaSalidaTrazaSerializer(many=False, read_only=True)
    linea_inventario = LineaInventarioTrazaSerializer(many=False, read_only=True)
    linea_pedido = LineaPedidoTrazaSerilizer(many=False, read_only=True)
    usuario = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Movimiento
        fields = ['id', 'fecha', 'cantidad', 'almacen', 'usuario', 'linea_pedido', 'linea_inventario', 'linea_salida', 'albaran']        

class PrecioRepuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecioRepuesto
        fields = ['id', 'proveedor', 'repuesto', 'precio', 'descuento', 'descripcion_proveedor', 'modelo_proveedor', 'fabricante']

class RepuestoConPrecioSerializer(serializers.ModelSerializer):
    repuesto = RepuestoListSerializer(many=False, read_only=True) 
    proveedor = ProveedorSerializer(many=False, read_only=True)
    class Meta:
        model = PrecioRepuesto
        fields = ['id', 'proveedor', 'repuesto', 'precio', 'descuento' , 'descripcion_proveedor', 'modelo_proveedor', 'fabricante']