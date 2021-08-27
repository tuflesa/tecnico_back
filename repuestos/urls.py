from rest_framework import routers
from .views import InventarioViewSet, MovimientoViewSet, RepuestoListViewSet, RepuestoDetailViewSet, StockMinimoViewSet, AlmacenViewSet, LineaInventarioViewSet

router = routers.DefaultRouter()
router.register('lista', RepuestoListViewSet)
router.register('detalle', RepuestoDetailViewSet)
router.register('stocks_minimos', StockMinimoViewSet)
router.register('almacen', AlmacenViewSet)
router.register('inventario', InventarioViewSet)
router.register('lineainventario', LineaInventarioViewSet)
router.register('movimiento', MovimientoViewSet)

urlpatterns = router.urls