from rest_framework import routers
from .views import EntregaViewSet, LineaAdicionalPedidoViewSet, MovimientoDetailViewSet, PedidoViewSet, InventarioViewSet, LineaPedidoViewSet, PedidoDetailViewSet, ContactoViewSet, MovimientoViewSet, PedidoListViewSet, ProveedorDetailViewSet, ProveedorViewSet, RepuestoListViewSet, RepuestoDetailViewSet, StockMinimoDetailViewSet, StockMinimoViewSet, AlmacenViewSet, LineaInventarioViewSet, TipoRepuestoViewSet

router = routers.DefaultRouter()
router.register('pedido', PedidoViewSet)
router.register('linea_adicional_pedido', LineaAdicionalPedidoViewSet)
router.register('movimiento', MovimientoViewSet)
router.register('entrega', EntregaViewSet)
router.register('linea_pedido', LineaPedidoViewSet)
router.register('lista', RepuestoListViewSet)
router.register('detalle', RepuestoDetailViewSet)
router.register('tipo_repuesto', TipoRepuestoViewSet)
router.register('stocks_minimos', StockMinimoViewSet)
router.register('almacen', AlmacenViewSet)
router.register('inventario', InventarioViewSet)
router.register('lineainventario', LineaInventarioViewSet)
router.register('movimiento_detalle', MovimientoDetailViewSet)
router.register('proveedor', ProveedorViewSet)
router.register('proveedor_detalle', ProveedorDetailViewSet)
router.register('contacto', ContactoViewSet)
router.register('lista_pedidos', PedidoListViewSet)
router.register('pedido_detalle', PedidoDetailViewSet)
router.register('stocks_minimo_detalle', StockMinimoDetailViewSet)


urlpatterns = router.urls