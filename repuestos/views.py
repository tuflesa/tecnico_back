from django.db.models import fields
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.serializers import Serializer
from .serializers import MovimientoDetailSerializer, StockMinimoDetailSerializer, PedidoSerilizer, LineaPedidoSerilizer, PedidoListSerilizer, PedidoDetailSerilizer, ProveedorDetailSerializer, AlmacenSerilizer, ContactoSerializer, InventarioSerializer, MovimientoSerializer, ProveedorSerializer, RepuestoListSerializer, RepuestoDetailSerializer, StockMinimoDetailSerializer, StockMinimoSerializer, LineaInventarioSerializer, TipoRepuestoSerilizer
from .models import Almacen, Inventario, Contacto, LineaInventario, LineaPedido, Movimiento, Pedido, Proveedor, Repuesto, StockMinimo, TipoRepuesto
from django_filters import filterset, rest_framework as filters

class AlmacenFilter(filters.FilterSet):
    class Meta:
        model = Almacen
        fields = {
            'empresa': ['exact'],
            'nombre': ['icontains']
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

class MovimientoDetailFilter(filters.FilterSet):
    class Meta:
        model = Movimiento
        fields = {
            'linea_pedido__id': ['exact'],
            'almacen__nombre' : ['exact']
        }

class RepuestoListFilter(filters.FilterSet):
    class Meta:
        model = Repuesto
        fields = {
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
            'proveedores__id':['exact']
        }

class PedidoListFilter(filters.FilterSet):
    class Meta:
        model = Pedido
        fields = {
            'proveedor__nombre': ['icontains'],
            'fecha_creacion': ['lte', 'gte'],
            'finalizado': ['exact'],
            'empresa': ['exact'],
            'numero': ['icontains']
        }

class StockMinimoFilter(filters.FilterSet):
    class Meta:
        model = StockMinimo
        fields = {
            'almacen__empresa__id':['exact'],
            'repuesto':['exact'],
            'almacen__nombre': ['exact']
        }

class TipoRepuestoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoRepuestoSerilizer
    queryset = TipoRepuesto.objects.all()

class RepuestoListViewSet(viewsets.ModelViewSet):
    serializer_class = RepuestoListSerializer
    queryset = Repuesto.objects.all().distinct()
    filterset_class = RepuestoListFilter

class RepuestoDetailViewSet(viewsets.ModelViewSet):
    serializer_class = RepuestoDetailSerializer
    queryset = Repuesto.objects.all()

class StockMinimoViewSet(viewsets.ModelViewSet):
    serializer_class = StockMinimoSerializer
    queryset = StockMinimo.objects.all()

class StockMinimoDetailViewSet(viewsets.ModelViewSet):
    serializer_class = StockMinimoDetailSerializer
    queryset = StockMinimo.objects.all()
    filterset_class = StockMinimoFilter

class AlmacenViewSet(viewsets.ModelViewSet):
    serializer_class = AlmacenSerilizer
    queryset = Almacen.objects.all()
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

class MovimientoDetailViewSet(viewsets.ModelViewSet):
    serializer_class = MovimientoDetailSerializer
    queryset = Movimiento.objects.all()
    filterset_class = MovimientoDetailFilter

class ProveedorViewSet(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    queryset = Proveedor.objects.all()
    filterset_class = ProveedorFilter

class ProveedorDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ProveedorDetailSerializer
    queryset = Proveedor.objects.all()

class ContactoViewSet(viewsets.ModelViewSet):
    serializer_class = ContactoSerializer
    queryset = Contacto.objects.all()

class PedidoListViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoListSerilizer
    queryset = Pedido.objects.all()
    filterset_class = PedidoListFilter

class PedidoDetailViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoDetailSerilizer
    queryset = Pedido.objects.all()

class LineaPedidoViewSet(viewsets.ModelViewSet):
    serializer_class = LineaPedidoSerilizer
    queryset = LineaPedido.objects.all()

class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerilizer
    queryset = Pedido.objects.all()