from django.db.models import fields
from rest_framework import viewsets
from rest_framework import serializers
#from django.db.models import Q, F
from django.db.models import Exists, OuterRef, Q, F
from rest_framework.serializers import Serializer
from .serializers import LineaPedidoDetailSerilizer, LineasAdicionalesDetalleSerilizer, RepuestoConPrecioSerializer, PrecioRepuestoSerializer, MovimientoTrazabilidadSerializer, LineaPedidoPendSerilizer, EntregaSerializer, LineasAdicionalesSerilizer, MovimientoDetailSerializer, SalidasSerializer, StockMinimoDetailSerializer, PedidoSerilizer, LineaPedidoSerilizer, PedidoListSerilizer, PedidoDetailSerilizer, ProveedorDetailSerializer, AlmacenSerilizer, ContactoSerializer, InventarioSerializer, MovimientoSerializer, ProveedorSerializer, RepuestoListSerializer, RepuestoDetailSerializer, StockMinimoDetailSerializer, StockMinimoSerializer, LineaInventarioSerializer, TipoRepuestoSerilizer, TipoUnidadSerilizer, LineaSalidaSerializer, LineaSalidaTrazaSerializer, SinStockMinimoSerializer, PedidoPorAlbaranSerilizer
from .models import PrecioRepuesto, Almacen, Entrega, Inventario, Contacto, LineaAdicional, LineaInventario, LineaPedido, Movimiento, Pedido, Proveedor, Repuesto, StockMinimo, TipoRepuesto, TipoUnidad, Salida, LineaSalida
from django_filters import filterset, rest_framework as filters
from rest_framework.pagination import PageNumberPagination
# En views.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny  # ← Añadir esta línea
from django.utils import timezone
from .models import ContadorPedidos

class ResetContadoresViewSet(ViewSet):
    """ViewSet temporal para resetear contadores"""
    permission_classes = [AllowAny]  # ← Añadir esta línea
    
    def list(self, request):
        year = timezone.now().year
        count = ContadorPedidos.objects.filter(year=year).update(contador=0)
        return Response({
            'message': f'Se resetearon {count} contadores para el año {year}'
        })

class AlmacenFilter(filters.FilterSet):
    class Meta:
        model = Almacen
        fields = {
            'empresa': ['exact'],
            'nombre': ['icontains'],
        }

class salidas_numparteFilter(filters.FilterSet):
    class Meta:
        model = LineaSalida
        fields = {
            'salida__num_parte': ['exact'],
        }
        
class ProveedorFilter(filters.FilterSet):
    class Meta:
        model = Proveedor
        fields = {
            'nombre': ['icontains'],
            'pais':['exact'],
            'de_rectificado':['exact'],
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
            'linea_salida__salida__num_parte': ['exact'],
        }

class RepuestoListFilter(filters.FilterSet):
    class Meta:
        model = Repuesto
        fields = {
            'id': ['exact'],
            'nombre': ['icontains'],
            'tipo_repuesto': ['exact'],
            'precios__fabricante': ['icontains'],
            'precios__modelo_proveedor': ['icontains'],
            'precios__proveedor':['exact'], 
            'precios__descripcion_proveedor':['icontains'],
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
            'empresa__id': ['exact'],
            'numero': ['icontains'],
            'lineas_pedido':['exact'],
            'lineas_pedido__cantidad':['exact'],
            'creado_por':['exact'],
            'descripcion':['icontains'],
            'intervencion': ['exact'],
            'revisado': ['exact'],
        }

class LineaPedidoFilter(filters.FilterSet):
    class Meta:
        model = LineaPedido
        fields = {
            'por_recibir': ['exact'],
            'cantidad': ['exact'],
            'pedido__finalizado': ['exact'],
            'pedido__numero': ['exact'],
            'pedido__numero': ['icontains'],
            'pedido__empresa': ['exact'],
            'pedido__creado_por': ['exact'],
            'repuesto': ['exact'],
            'pedido__proveedor': ['exact'],
            'pedido__fecha_prevista_entrega': ['exact'],
            'pedido__empresa__id': ['exact'],
            'descripcion_proveedor': ['icontains'],
            'repuesto__tipo_repuesto': ['exact'],
            'pedido__proveedor__nombre':['icontains'],
        }
class PedidoPorAlbaranFilter(filters.FilterSet):
    numero_albaran = filters.CharFilter(method='filtro_por_albaran')
    class Meta:
        model = Pedido
        fields = {
            'empresa__id': ['exact'],
            'proveedor__nombre':['icontains'],
        }
    def filtro_por_albaran(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(lineas_pedido__movimiento__albaran__icontains=value) |
                Q(lineas_adicionales__entregas__albaran__icontains=value)
            ).distinct()
        return queryset

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
            'cantidad_aconsejable': ['exact'],
            'repuesto__descatalogado' : ['exact'],
            'repuesto__nombre' : ['icontains'],
            'repuesto__fabricante' : ['icontains'],
            'almacen__nombre' : ['icontains'],
            'repuesto__nombre_comun' : ['icontains'],
            'almacen__empresa':['exact'],
            'repuesto__tipo_repuesto': ['exact'],
            'repuesto__es_critico' : ['exact'],
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
            'proveedor__nombre':['exact'],
            'proveedor__nombre':['icontains'],
            'repuesto__nombre':['icontains'],
            'proveedor__id':['exact'],
            'repuesto__id':['exact'],
            'repuesto__modelo':['icontains'],
            'descripcion_proveedor': ['icontains'],
            'modelo_proveedor': ['icontains'],
            'repuesto__descatalogado':['exact'],
            'repuesto__tipo_repuesto': ['exact'],
            'repuesto__fabricante': ['icontains'],
            'repuesto__es_critico': ['exact'],
            'repuesto__equipos__seccion__zona__empresa__id' : ['exact'],
            'repuesto__equipos__seccion__zona__id': ['exact'],
            'repuesto__equipos__seccion__id': ['exact'],
            'repuesto__equipos__id': ['exact'],
            'repuesto__proveedores__id':['exact'],
            'repuesto__nombre_comun':['icontains'],
        }

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000 

class TipoRepuestoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoRepuestoSerilizer
    queryset = TipoRepuesto.objects.all()

class TipoUnidadViewSet(viewsets.ModelViewSet):
    serializer_class = TipoUnidadSerilizer
    queryset = TipoUnidad.objects.all()

class RepuestoListViewSet(viewsets.ModelViewSet):
    serializer_class = RepuestoListSerializer
    queryset = Repuesto.objects.all().order_by('nombre').distinct()
    filterset_class = RepuestoListFilter
    pagination_class = StandardResultsSetPagination

class RepuestoListSinPaginarViewSet(viewsets.ModelViewSet):
    serializer_class = RepuestoListSerializer
    queryset = Repuesto.objects.all().order_by('nombre')
    filterset_class = RepuestoListFilter

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
    queryset = StockMinimo.objects.filter(Q(stock_act__lt=F('cantidad_aconsejable')) | Q(stock_act__lt=F('cantidad'))).order_by('repuesto__nombre')
    filterset_class = StockMinimoFilter
    pagination_class = StandardResultsSetPagination

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
    queryset = Proveedor.objects.all().order_by('nombre')

class ContactoViewSet(viewsets.ModelViewSet):
    serializer_class = ContactoSerializer
    queryset = Contacto.objects.all()
    filterset_class = ContactosFilter

class PedidoListViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoListSerilizer
    queryset = Pedido.objects.all().order_by('numero')
    filterset_class = PedidoListFilter

class PedidoFueraFechaViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoListSerilizer
    queryset = Pedido.objects.all().order_by('-numero')
    filterset_class = PedidoListFilter
    pagination_class = StandardResultsSetPagination

class PedidoDetailViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoDetailSerilizer
    queryset = Pedido.objects.all().order_by('numero')
    filterset_class = PedidoListFilter

class LineaPedidoViewSet(viewsets.ModelViewSet):
    serializer_class = LineaPedidoSerilizer
    queryset = LineaPedido.objects.all().order_by('id')
    filterset_class = LineaPedidoFilter

class LineaPedidoDetalleViewSet(viewsets.ModelViewSet):
    serializer_class = LineaPedidoDetailSerilizer
    queryset = LineaPedido.objects.all().order_by('id')
    filterset_class = LineaPedidoFilter

class LineaPedidoPendViewSet(viewsets.ModelViewSet):
    serializer_class = LineaPedidoPendSerilizer
    queryset = LineaPedido.objects.all().order_by('id')
    filterset_class = LineaPedidoFilter

class LineaAdicionalPedidoViewSet(viewsets.ModelViewSet):
    serializer_class = LineasAdicionalesSerilizer
    queryset = LineaAdicional.objects.all().order_by('id')

class LineaAdicionalDetalleViewSet(viewsets.ModelViewSet):
    serializer_class = LineasAdicionalesDetalleSerilizer
    queryset = LineaAdicional.objects.all().order_by('descripcion')
    filterset_class = LineaAdicionalFilter
    pagination_class = StandardResultsSetPagination

class PedidoPorAlbaranViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoPorAlbaranSerilizer
    queryset = Pedido.objects.all().order_by('numero')
    filterset_class = PedidoPorAlbaranFilter
    pagination_class = StandardResultsSetPagination

class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerilizer
    queryset = Pedido.objects.all().order_by('numero')

class SalidaVieSet(viewsets.ModelViewSet):
    serializer_class = SalidasSerializer
    queryset = Salida.objects.all()

class LineasSalidaVieSet(viewsets.ModelViewSet):
    serializer_class = LineaSalidaSerializer
    queryset = LineaSalida.objects.all()

class LineasSalida_numparteVieSet(viewsets.ModelViewSet):
    serializer_class = LineaSalidaTrazaSerializer
    queryset = LineaSalida.objects.all()
    filterset_class = salidas_numparteFilter

class MovimientoTrazabilidadViewSet(viewsets.ModelViewSet):
    serializer_class = MovimientoTrazabilidadSerializer
    queryset = Movimiento.objects.all()
    filterset_class = MovimientoTrazabilidadFilter

class PrecioRepuestoViewSet(viewsets.ModelViewSet):
    serializer_class = PrecioRepuestoSerializer
    queryset = PrecioRepuesto.objects.all().order_by('repuesto__nombre')
    filterset_class = PrecioRepuestoFilter

class RepuestoConPrecioViewSet(viewsets.ModelViewSet):
    serializer_class = RepuestoConPrecioSerializer
    #queryset = PrecioRepuesto.objects.all().order_by('repuesto__nombre').distinct()
    queryset = PrecioRepuesto.objects.all().distinct()  # Solo para DRF
    filterset_class = PrecioRepuestoFilter
    def get_queryset(self):
        user = self.request.user
        empresa = user.perfil.empresa
        cond_subquery = StockMinimo.objects.filter(
            repuesto=OuterRef('repuesto'),
            almacen__empresa=empresa
        ).filter(
            Q(stock_act__lt=F('cantidad_aconsejable')) | Q(stock_act__lt=F('cantidad'))
        )

        cond_pedido = LineaPedido.objects.filter(
            repuesto=OuterRef('repuesto'),
            por_recibir__gt=0,
            pedido__finalizado=False,
            pedido__empresa=empresa
        )

        return PrecioRepuesto.objects.annotate(
            necesita_stock=Exists(cond_subquery),
            pedido=Exists(cond_pedido)
        ).order_by('-necesita_stock', 'repuesto__nombre').select_related('repuesto').distinct()

""" class RepuestoPrecioStockViewSet(viewsets.ModelViewSet):
    serializer_class = RepuestoPrecioStockSerializer
    queryset = PrecioRepuesto.objects.all().order_by('repuesto__nombre').distinct()
    filterset_class = PrecioRepuestoFilter
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context  # Esto ya incluye 'request' por defecto """

class Filtro_RepuestoConPrecioViewSet(viewsets.ModelViewSet):
    serializer_class = RepuestoConPrecioSerializer
    queryset = PrecioRepuesto.objects.all().order_by('repuesto__nombre')
    filterset_class = PrecioRepuestoFilter
    pagination_class = StandardResultsSetPagination