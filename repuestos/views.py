from rest_framework import viewsets
from rest_framework.serializers import Serializer
from .serializers import AlmacenSerilizer, InventarioSerializer, MovimientoSerializer, RepuestoListSerializer, RepuestoDetailSerializer, StockMinimoSerializer, LineaInventarioSerializer
from .models import Almacen, Inventario, LineaInventario, Movimiento, Repuesto, StockMinimo
from django_filters import rest_framework as filters

class AlmacenFilter(filters.FilterSet):
    class Meta:
        model = Almacen
        fields = {
            'empresa': ['exact']
        }

class RepuestoListViewSet(viewsets.ModelViewSet):
    serializer_class = RepuestoListSerializer
    queryset = Repuesto.objects.all()

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
