from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.serializers import Serializer
from .serializers import PedidoListSerilizer, PedidoDetailSerilizer, ProveedorDetailSerializer, AlmacenSerilizer, ContactoSerializer, InventarioSerializer, MovimientoSerializer, ProveedorSerializer, RepuestoListSerializer, RepuestoDetailSerializer, StockMinimoSerializer, LineaInventarioSerializer, TipoRepuestoSerilizer
from .models import Almacen, Inventario, Contacto, LineaInventario, Movimiento, Pedido, Proveedor, Repuesto, StockMinimo, TipoRepuesto
from django_filters import rest_framework as filters

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
            'equipos__id': ['exact']
        }

class PedidoListFilter(filters.FilterSet):
    class Meta:
        model = Pedido
        fields = {
            'proveedor__nombre': ['icontains'],
            'fecha_creacion': ['lte', 'gte'],
            'finalizado': ['exact']
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