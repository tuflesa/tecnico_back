from rest_framework import viewsets
from rest_framework.serializers import Serializer
from .serializers import AlmacenSerilizer, InventarioSerializer, MovimientoSerializer, ProveedorSerializer, RepuestoListSerializer, RepuestoDetailSerializer, StockMinimoSerializer, LineaInventarioSerializer
from .models import Almacen, Inventario, LineaInventario, Movimiento, Proveedor, Repuesto, StockMinimo
from django_filters import rest_framework as filters

class AlmacenFilter(filters.FilterSet):
    class Meta:
        model = Almacen
        fields = {
            'empresa': ['exact']
        }

class RepuestoListFilter(filters.FilterSet):
    class Meta:
        model = Repuesto
        fields = {
            'nombre': ['icontains'],
            'fabricante': ['icontains'],
            'modelo': ['icontains'],
            'es_critico': ['exact'],
            'descatalogado': ['exact'],
            'equipos__seccion__zona__empresa__id' : ['exact'],
            'equipos__seccion__zona__id': ['exact'],
            'equipos__seccion__id': ['exact'],
            'equipos__id': ['exact']
        }

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
