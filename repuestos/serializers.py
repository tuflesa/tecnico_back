from django.db.models import fields
from django.db.models.base import Model
from estructura.serializers import DireccionesEmpresaSerializer, EmpresaSerializer, EquipoSerializer
from rest_framework import serializers
from .models import PrecioRepuesto, Entrega, LineaAdicional, Almacen, Contacto, Inventario, LineaPedido, LineaSalida, Movimiento, Pedido, Repuesto, Proveedor, Salida, StockMinimo, LineaInventario, TipoRepuesto, TipoUnidad
from estructura.serializers import EquipoSerializer
from estructura.serializers import EstructuraSerializer
from estructura.serializers import EmpresaSerializer
from administracion.serializers import UserSerializer
from mantenimiento.serializers import ParteTrabajoSerializer

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
        fields = '__all__' 

class ProveedorRepuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProveedorDetailSerializer(serializers.ModelSerializer):
    contactos = ContactoSerializer(many=True, read_only=True)
    class Meta:
        model = Proveedor
        fields = '__all__'
class AlmacenSerilizer(serializers.ModelSerializer):
    # empresa = EmpresaSerializer(many=False, read_only=False)
    class Meta:
        model = Almacen
        fields = '__all__'

class SinStockMinimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMinimo
        fields = '__all__'
class StockMinimoAlmacenSerializer(serializers.ModelSerializer):
    almacen = AlmacenSerilizer(many=False)
    class Meta:
        model = StockMinimo
        fields = '__all__'

class PrecioRepuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecioRepuesto
        fields = '__all__'
        
class RepuestoListSerializer(serializers.ModelSerializer):
    tipo_unidad_siglas = serializers.CharField(source='tipo_unidad.siglas', read_only=True)
    precios = PrecioRepuestoSerializer(many=True)
    class Meta:
        model = Repuesto
        fields = '__all__'

class StockMinimoDetailSerializer(serializers.ModelSerializer):
    almacen = AlmacenSerilizer(many=False, read_only=True)
    repuesto = RepuestoListSerializer(many=False, read_only=True)
    class Meta:
        model = StockMinimo
        fields = '__all__'
class LineaPedidoSerilizer(serializers.ModelSerializer):
    #pedido = PedidoListSerilizer(many=False, read_only=True)
    class Meta:
        model = LineaPedido
        fields = '__all__'
class RepuestoList_PedidoSerializer(serializers.ModelSerializer):
    tipo_unidad_siglas = serializers.CharField(source='tipo_unidad.siglas', read_only=True)
    precios = PrecioRepuestoSerializer(many=True)
    stocks_minimos = StockMinimoDetailSerializer(many=True, read_only=True)
    lineas_repuesto = LineaPedidoSerilizer(many=True)
    class Meta:
        model = Repuesto
        fields = '__all__'

class StockMinimoSerializer(serializers.ModelSerializer):
    #almacen = AlmacenSerilizer(many=False, read_only=True)
    class Meta:
        model = StockMinimo
        fields = '__all__'

class RepuestoDetailSerializer(serializers.ModelSerializer):
    equipos = EquipoSerializer(many=True, read_only=True)
    proveedores = ProveedorSerializer(many=True, read_only=True)
    stocks_minimos = StockMinimoDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Repuesto
        fields = '__all__'

class TipoRepuestoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = TipoRepuesto
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'

class LineaInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaInventario
        fields = '__all__'

class LineaInventarioTrazaSerializer(serializers.ModelSerializer):
    inventario = InventarioSerializer(many=False, read_only=True)
    class Meta:
        model = LineaInventario
        fields = '__all__'

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__'

class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = '__all__'

class MovimientoDetailSerializer(serializers.ModelSerializer):
    almacen = AlmacenSerilizer(many=False, read_only=True)
    class Meta:
        model = Movimiento
        fields = '__all__'      

class PedidoListSerilizer(serializers.ModelSerializer):
    empresa = EstructuraSerializer(many=False, read_only=True)
    proveedor = ProveedorSerializer(many=False, read_only=True)
    creado_por = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Pedido
        fields = '__all__'
class LineaPedidoDetailSerilizer(serializers.ModelSerializer):
    tipo_unidad_nombre = serializers.CharField(source='tipo_unidad.siglas', read_only=True)
    repuesto = RepuestoListSerializer(many=False, read_only=True)    
    class Meta:
        model = LineaPedido
        fields = '__all__'

class LineaPedidoTrazaSerilizer(serializers.ModelSerializer):
    repuesto = RepuestoListSerializer(many=False, read_only=True)    
    pedido = PedidoListSerilizer(many=False, read_only=True)
    class Meta:
        model = LineaPedido
        fields = '__all__'

class LineaPedidoPendSerilizer(serializers.ModelSerializer):
    repuesto = RepuestoListSerializer(many=False, read_only=True) 
    pedido = PedidoListSerilizer(many=False, read_only=True)
    class Meta:
        model = LineaPedido
        fields = '__all__'

class LineasAdicionalesSerilizer(serializers.ModelSerializer):
    class Meta:
        model = LineaAdicional
        fields = '__all__'

class LineasAdicionalesDetalleSerilizer(serializers.ModelSerializer):
    pedido = PedidoListSerilizer(many=False, read_only=True)
    class Meta:
        model = LineaAdicional
        fields = '__all__'
class LineasAdicionalesAlbaranSerilizer(serializers.ModelSerializer):
    entregas = EntregaSerializer(many=True)
    class Meta:
        model = LineaAdicional
        fields = '__all__'
class LineasPedidoPorAlbaranSerilizer(serializers.ModelSerializer):
    movimiento = MovimientoSerializer (many=True)
    class Meta:
        model = LineaPedido
        fields = '__all__'
class PedidoPorAlbaranSerilizer(serializers.ModelSerializer):
    lineas_pedido = LineasPedidoPorAlbaranSerilizer (many=True)
    lineas_adicionales = LineasAdicionalesAlbaranSerilizer (many=True)
    proveedor = ProveedorSerializer(many=False, read_only=True)
    empresa = EmpresaSerializer(many=False)
    creado_por = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Pedido
        fields = '__all__'
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
        fields = '__all__'

class PedidoSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
class SalidasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salida
        fields = '__all__'

class SalidasTrazaSerializer(serializers.ModelSerializer):
    num_parte = ParteTrabajoSerializer(many=False)
    class Meta:
        model = Salida
        fields = '__all__'

class LineaSalidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaSalida
        fields = '__all__'
class LineaSalidaTrazaSerializer(serializers.ModelSerializer):
    salida = SalidasTrazaSerializer(many=False, read_only=True)
    repuesto = RepuestoListSerializer(many=False, read_only=True)
    class Meta:
        model = LineaSalida
        fields = fields = '__all__'

class MovimientoTrazabilidadSerializer(serializers.ModelSerializer):
    almacen = AlmacenSerilizer(many=False, read_only=True)
    linea_salida = LineaSalidaTrazaSerializer(many=False, read_only=True)
    linea_inventario = LineaInventarioTrazaSerializer(many=False, read_only=True)
    linea_pedido = LineaPedidoTrazaSerilizer(many=False, read_only=True)
    usuario = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Movimiento
        fields = fields = '__all__'       

class RepuestoSinStockSerializer(serializers.ModelSerializer): #saca los repuesto con los stock minimos que esten a cero por almacén
    stocks_minimos = serializers.SerializerMethodField()

    class Meta:
        model = Repuesto
        fields = '__all__'

    def get_stocks_minimos(self, obj):
        stock_filtrado = obj.stocks_minimos.filter(stock_act=0)
        return SinStockMinimoSerializer(stock_filtrado, many=True).data

class RepuestoConPrecioSerializer(serializers.ModelSerializer):
    repuesto = RepuestoList_PedidoSerializer(many=False, read_only=True) 
    proveedor = ProveedorSerializer(many=False, read_only=True)
    necesita_stock = serializers.BooleanField(read_only=True) # Campo creado en la views que ve los articulos por debajo de stock minimo
    pedido = serializers.BooleanField(read_only=True) # Campo creado en la views, será true si tenemos linea en pedidos con por_recibir > 0
    class Meta:
        model = PrecioRepuesto
        fields = '__all__'

""" class RepuestoDetailPrecioStockSerializer(serializers.ModelSerializer):
    equipos = EquipoSerializer(many=True, read_only=True)
    proveedores = ProveedorSerializer(many=True, read_only=True)
    stocks_minimos = StockMinimoDetailSerializer(many=True, read_only=True)
    stock_total = serializers.SerializerMethodField()
    
    class Meta:
        model = Repuesto
        fields = '__all__'
    
    def get_stock_total(self, obj):
        # Obtenemos la empresa del usuario que hace la petición
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return 0
        
        try:
            empresa_id = request.user.perfil.empresa.id
        except AttributeError:
            return 0
        
        # Sumamos el stock_act de todos los stocks_minimos que pertenecen a la empresa del usuario
        total_stock = 0
        for stock in obj.stocks_minimos.all():
            if stock.almacen and stock.almacen.empresa_id == empresa_id:
                total_stock += stock.stock_act or 0
                
        return total_stock """
    
""" class RepuestoPrecioStockSerializer(serializers.ModelSerializer):
    repuesto = serializers.SerializerMethodField()
    proveedor = ProveedorSerializer(many=False, read_only=True)
    
    class Meta:
        model = PrecioRepuesto
        fields = '__all__'
    
    def get_repuesto(self, obj):
        # Pasamos el contexto de la solicitud al serializador de repuesto
        return RepuestoDetailPrecioStockSerializer(obj.repuesto, context=self.context).data """