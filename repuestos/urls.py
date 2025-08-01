from rest_framework import routers
from .views import ResetContadoresViewSet,RepuestoListSinPaginarViewSet, Filtro_RepuestoConPrecioViewSet, LineaPedidoDetalleViewSet, LineaAdicionalDetalleViewSet, RepuestoConPrecioViewSet, PrecioRepuestoViewSet, MovimientoTrazabilidadViewSet, ArticulosFueraStockViewSet, LineaPedidoPendViewSet, EntregaViewSet, LineaAdicionalPedidoViewSet, LineasSalidaVieSet, MovimientoDetailViewSet, PedidoViewSet, InventarioViewSet, LineaPedidoViewSet, PedidoDetailViewSet, ContactoViewSet, MovimientoViewSet, PedidoListViewSet, ProveedorDetailViewSet, ProveedorViewSet, RepuestoListViewSet, RepuestoDetailViewSet, SalidaVieSet, StockMinimoDetailViewSet, StockMinimoViewSet, AlmacenViewSet, LineaInventarioViewSet, TipoRepuestoViewSet, TipoUnidadViewSet, PedidoFueraFechaViewSet, LineasSalida_numparteVieSet, PedidoPorAlbaranViewSet

router = routers.DefaultRouter()
router.register('reset-contadores', ResetContadoresViewSet, basename='reset-contadores') #http://localhost:8000/api/repuestos/reset-contadores/
router.register('pedido', PedidoViewSet)
router.register('lineas_salidas', LineasSalida_numparteVieSet)
router.register('pedidos_por_albaran', PedidoPorAlbaranViewSet)
router.register('linea_pedido_pend', LineaPedidoPendViewSet)
router.register('repuesto_precio', RepuestoConPrecioViewSet)
""" router.register('repuesto_precio_stock', RepuestoPrecioStockViewSet) """
router.register('filtro_repuesto_precio', Filtro_RepuestoConPrecioViewSet)
router.register('precio_detalle', PrecioRepuestoViewSet)
router.register('precio', PrecioRepuestoViewSet)
router.register('tipo_unidad', TipoUnidadViewSet)
router.register('linea_adicional_detalle', LineaAdicionalDetalleViewSet)
router.register('linea_adicional_pedido', LineaAdicionalPedidoViewSet)
router.register('movimiento', MovimientoViewSet)
router.register('entrega', EntregaViewSet)
router.register('linea_pedido_detalle', LineaPedidoDetalleViewSet)
router.register('linea_pedido', LineaPedidoViewSet)
router.register('lista_repuestos', RepuestoListSinPaginarViewSet)
router.register('lista', RepuestoListViewSet)
router.register('detalle', RepuestoDetailViewSet)
router.register('tipo_repuesto', TipoRepuestoViewSet)
router.register('stocks_minimos', StockMinimoViewSet)
router.register('almacen', AlmacenViewSet)
router.register('inventario', InventarioViewSet)
router.register('lineainventario', LineaInventarioViewSet)
router.register('movimiento_trazabilidad', MovimientoTrazabilidadViewSet)
router.register('movimiento_detalle', MovimientoDetailViewSet)
router.register('proveedor', ProveedorViewSet)
router.register('proveedor_detalle', ProveedorDetailViewSet)
router.register('contacto', ContactoViewSet)
router.register('lista_pedidos_fuera_fecha', PedidoFueraFechaViewSet)
router.register('lista_pedidos', PedidoListViewSet)
router.register('pedido_detalle', PedidoDetailViewSet)
router.register('articulos_fuera_stock',ArticulosFueraStockViewSet)
router.register('stocks_minimo_detalle', StockMinimoDetailViewSet)
router.register('salida', SalidaVieSet)
router.register('lineasalida', LineasSalidaVieSet)


urlpatterns = router.urls