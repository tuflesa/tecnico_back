from django.db.models import fields
from rest_framework import viewsets
from rest_framework import serializers
from django.db.models import F
from rest_framework.serializers import Serializer
from .serializers import LineasAdicionalesDetalleSerilizer, RepuestoConPrecioSerializer, PrecioRepuestoSerializer, MovimientoTrazabilidadSerializer, LineaPedidoPendSerilizer, EntregaSerializer, LineasAdicionalesSerilizer, MovimientoDetailSerializer, SalidasSerializer, StockMinimoDetailSerializer, PedidoSerilizer, LineaPedidoSerilizer, PedidoListSerilizer, PedidoDetailSerilizer, ProveedorDetailSerializer, AlmacenSerilizer, ContactoSerializer, InventarioSerializer, MovimientoSerializer, ProveedorSerializer, RepuestoListSerializer, RepuestoDetailSerializer, StockMinimoDetailSerializer, StockMinimoSerializer, LineaInventarioSerializer, TipoRepuestoSerilizer, TipoUnidadSerilizer, LineaSalidaSerializer
from .models import PrecioRepuesto, Almacen, Entrega, Inventario, Contacto, LineaAdicional, LineaInventario, LineaPedido, Movimiento, Pedido, Proveedor, Repuesto, StockMinimo, TipoRepuesto, TipoUnidad, Salida, LineaSalida
from django_filters import filterset, rest_framework as filters
from rest_framework.pagination import PageNumberPagination


class AlmacenFilter(filters.FilterSet):
    class Meta:
        model = Almacen
        fields = {
            'empresa': ['exact'],
            'nombre': ['icontains'],
        }
        
class ProveedorFilter(filters.FilterSet):
    class Meta:
        model = Proveedor
        fields = {
            'nombre': ['icontains']
        }

class MovimientoFilter(filters.FilterSet):
    class Meta:
        model = Movimiento
        fields = {
            'linea_pedido__id': ['exact']
        }

class EntregaFilter(filters.FilterSet):
    class Meta:
        model = Entrega
        fields = {
            'linea_adicional__id': ['exact']
        }

class MovimientoDetailFilter(filters.FilterSet):
    class Meta:
        model = Movimiento
        fields = {
            'linea_pedido__id': ['exact'],
            'almacen__nombre' : ['exact']
        }

class MovimientoTrazabilidadFilter(filters.FilterSet):
    class Meta:
        model = Movimiento
        fields = {            
            'linea_salida__repuesto' : ['exact'],
            'linea_inventario__repuesto':['exact'],
            'linea_pedido__repuesto':['exact'],
            'almacen__id': ['exact'],
        }

class RepuestoListFilter(filters.FilterSet):
    class Meta:
        model = Repuesto
        fields = {
            'id': ['exact'],
            'nombre': ['icontains'],
            'tipo_repuesto': ['exact'],
            'fabricante': ['icontains'],
            'modelo': ['icontains'],
            'es_critico': ['exact'],
            'descatalogado': ['exact'],
            'equipos__seccion__zona__empresa__id' : ['exact'],
            'equipos__seccion__zona__id': ['exact'],
            'equipos__seccion__id': ['exact'],
            'equipos__id': ['exact'],
            'proveedores__id':['exact'],
            'stocks_minimos__almacen__id':['exact'],
            'nombre_comun':['icontains'],
        }

class PedidoListFilter(filters.FilterSet):
    class Meta:
        model = Pedido
        fields = {
            'proveedor__nombre': ['icontains'],
            'fecha_creacion': ['lte', 'gte'],
            'fecha_prevista_entrega': ['lte', 'gte'],
            'finalizado': ['exact'],
            'empresa': ['exact'],
            'numero': ['icontains'],
            'lineas_pedido':['exact'],
            'lineas_pedido__cantidad':['exact'],
            'creado_por':['exact'],
            'descripcion':['icontains'],
        }

class LineaPedidoFilter(filters.FilterSet):
    class Meta:
        model = LineaPedido
        fields = {
            'por_recibir': ['exact'],
            'cantidad': ['exact'],
            'pedido__finalizado': ['exact'],
            'pedido__numero': ['exact'],
            'pedido__empresa': ['exact'],
            'pedido__creado_por': ['exact'],
            'repuesto': ['exact'],
            'pedido__proveedor': ['exact'],
            'pedido__fecha_prevista_entrega': ['exact'],
            'pedido__empresa__id': ['exact'],
        }

class LineaAdicionalFilter(filters.FilterSet):
    class Meta:
        model = LineaAdicional
        fields = {
            'por_recibir': ['exact'],
            'cantidad': ['exact'],
            'pedido__finalizado': ['exact'],
            'pedido__numero': ['icontains'],
            'pedido__empresa__id': ['exact'],
            'precio': ['exact'],
            'descuento': ['exact'],
            'total': ['exact'],
            'descripcion': ['icontains'],
            'pedido__proveedor__nombre':['icontains'],
        }

class StockMinimoFilter(filters.FilterSet):
    class Meta:
        model = StockMinimo
        fields = {
            'almacen__empresa__id':['exact'],
            'repuesto':['exact'],
            'repuesto__id': ['exact'],
            'repuesto__nombre' : ['exact'],
            'almacen__nombre': ['exact'],
            'almacen__id': ['exact'],
            'almacen': ['exact'],
            'almacen__empresa__siglas': ['exact'],
            'stock_act': ['lt', 'gt'],
            'cantidad': ['exact'],
            'repuesto__descatalogado' : ['exact'],
            'repuesto__nombre' : ['icontains'],
            'repuesto__fabricante' : ['icontains'],
            'almacen__nombre' : ['icontains'],
            'repuesto__nombre_comun' : ['icontains'],
            'almacen__empresa':['exact'],
        }

class ContactosFilter(filters.FilterSet):
    class Meta:
        model = Contacto
        fields = {
            'proveedor': ['exact']
        }

class PrecioRepuestoFilter(filters.FilterSet):
    class Meta:
        model = PrecioRepuesto
        fields = {
            'proveedor': ['exact'],
            'repuesto':['exact'],
            'proveedor__nombre':['icontains'],
            'repuesto__nombre':['icontains'],
            'proveedor__id':['exact'],
            'repuesto__id':['exact'],
            'repuesto__modelo':['icontains'],
        }

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    paginator=1
    max_page_size = 1000 

class TipoRepuestoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoRepuestoSerilizer
    queryset = TipoRepuesto.objects.all()

class TipoUnidadViewSet(viewsets.ModelViewSet):
    serializer_class = TipoUnidadSerilizer
    queryset = TipoUnidad.objects.all()

class RepuestoListViewSet(viewsets.ModelViewSet):
    serializer_class = RepuestoListSerializer
    queryset = Repuesto.objects.all().distinct().order_by('nombre')
    filterset_class = RepuestoListFilter
    pagination_class = StandardResultsSetPagination

class RepuestoDetailViewSet(viewsets.ModelViewSet):
    serializer_class = RepuestoDetailSerializer
    queryset = Repuesto.objects.all().order_by('nombre')
    filterset_class = RepuestoListFilter
    pagination_class = StandardResultsSetPagination
  
class StockMinimoViewSet(viewsets.ModelViewSet):
    serializer_class = StockMinimoSerializer
    queryset = StockMinimo.objects.all()
    filterset_class = StockMinimoFilter

class StockMinimoDetailViewSet(viewsets.ModelViewSet):
    serializer_class = StockMinimoDetailSerializer
    queryset = StockMinimo.objects.all().order_by('repuesto__nombre')
    filterset_class = StockMinimoFilter

class ArticulosFueraStockViewSet(viewsets.ModelViewSet):
    serializer_class = StockMinimoDetailSerializer
    queryset = StockMinimo.objects.filter(stock_act__lt=F('cantidad'))
    filterset_class = StockMinimoFilter

class AlmacenViewSet(viewsets.ModelViewSet):
    serializer_class = AlmacenSerilizer
    queryset = Almacen.objects.all().order_by('nombre')
    filterset_class = AlmacenFilter

class InventarioViewSet(viewsets.ModelViewSet):
    serializer_class = InventarioSerializer
    queryset = Inventario.objects.all()

class LineaInventarioViewSet(viewsets.ModelViewSet):
    serializer_class = LineaInventarioSerializer
    queryset = LineaInventario.objects.all()

class MovimientoViewSet(viewsets.ModelViewSet):
    serializer_class = MovimientoSerializer
    queryset = Movimiento.objects.all()
    filterset_class = MovimientoFilter

class EntregaViewSet(viewsets.ModelViewSet):
    serializer_class = EntregaSerializer
    queryset = Entrega.objects.all()
    filterset_class = EntregaFilter

class MovimientoDetailViewSet(viewsets.ModelViewSet):
    serializer_class = MovimientoDetailSerializer
    queryset = Movimiento.objects.all()
    filterset_class = MovimientoDetailFilter

class ProveedorViewSet(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    queryset = Proveedor.objects.all().order_by('nombre')
    filterset_class = ProveedorFilter

class ProveedorDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ProveedorDetailSerializer
    queryset = Proveedor.objects.all()

class ContactoViewSet(viewsets.ModelViewSet):
    serializer_class = ContactoSerializer
    queryset = Contacto.objects.all()
    filterset_class = ContactosFilter

class PedidoListViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoListSerilizer
    queryset = Pedido.objects.all().order_by('numero')
    filterset_class = PedidoListFilter

class PedidoDetailViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoDetailSerilizer
    queryset = Pedido.objects.all()
    filterset_class = PedidoListFilter

class LineaPedidoViewSet(viewsets.ModelViewSet):
    serializer_class = LineaPedidoSerilizer
    queryset = LineaPedido.objects.all()
    filterset_class = LineaPedidoFilter

class LineaPedidoPendViewSet(viewsets.ModelViewSet):
    serializer_class = LineaPedidoPendSerilizer
    queryset = LineaPedido.objects.all()
    filterset_class = LineaPedidoFilter

class LineaAdicionalPedidoViewSet(viewsets.ModelViewSet):
    serializer_class = LineasAdicionalesSerilizer
    queryset = LineaAdicional.objects.all()

class LineaAdicionalDetalleViewSet(viewsets.ModelViewSet):
    serializer_class = LineasAdicionalesDetalleSerilizer
    queryset = LineaAdicional.objects.all().order_by('descripcion')
    filterset_class = LineaAdicionalFilter

class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerilizer
    queryset = Pedido.objects.all()

class SalidaVieSet(viewsets.ModelViewSet):
    serializer_class = SalidasSerializer
    queryset = Salida.objects.all()

class LineasSalidaVieSet(viewsets.ModelViewSet):
    serializer_class = LineaSalidaSerializer
    queryset = LineaSalida.objects.all()

class MovimientoTrazabilidadViewSet(viewsets.ModelViewSet):
    serializer_class = MovimientoTrazabilidadSerializer
    queryset = Movimiento.objects.all()
    filterset_class = MovimientoTrazabilidadFilter

class PrecioRepuestoViewSet(viewsets.ModelViewSet):
    serializer_class = PrecioRepuestoSerializer
    queryset = PrecioRepuesto.objects.all()
    filterset_class = PrecioRepuestoFilter

class RepuestoConPrecioViewSet(viewsets.ModelViewSet):
    serializer_class = RepuestoConPrecioSerializer
    queryset = PrecioRepuesto.objects.all().order_by('repuesto__nombre')
    filterset_class = PrecioRepuestoFilter