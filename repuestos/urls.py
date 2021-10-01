from rest_framework import routers
from .views import InventarioViewSet, ContactoProveedorViewSet, MovimientoViewSet, ProveedorViewSet, RepuestoListViewSet, RepuestoDetailViewSet, StockMinimoViewSet, AlmacenViewSet, LineaInventarioViewSet, TipoRepuestoViewSet

router = routers.DefaultRouter()
router.register('lista', RepuestoListViewSet)
router.register('detalle', RepuestoDetailViewSet)
router.register('tipo_repuesto', TipoRepuestoViewSet)
router.register('stocks_minimos', StockMinimoViewSet)
router.register('almacen', AlmacenViewSet)
router.register('inventario', InventarioViewSet)
router.register('lineainventario', LineaInventarioViewSet)
router.register('movimiento', MovimientoViewSet)
router.register('proveedor', ProveedorViewSet)
router.register('contacto', ContactoProveedorViewSet)

urlpatterns = router.urls