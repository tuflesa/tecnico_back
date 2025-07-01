from django.contrib import admin
from .models import PrecioRepuesto, Entrega, LineaAdicional, ContadorPedidos, LineaSalida, Repuesto, Proveedor, Contacto, Pedido, LineaPedido, Movimiento, Almacen, Inventario, LineaInventario, Salida, StockMinimo, TipoRepuesto, TipoUnidad

class PedidoAdmin(admin.ModelAdmin):
    search_fields=("numero",)
    list_display=("proveedor", "numero",)
    list_filter=("proveedor",)

class LineaPedidoAdmin(admin.ModelAdmin):
    search_fields=("repuesto__nombre",)
    search_fields=("pedido__numero",)
    list_display=("repuesto", "pedido",)

class StockMinimoAdmin(admin.ModelAdmin):
    search_fields=("repuesto__nombre",)

class MovimientoAdmin(admin.ModelAdmin):
    list_filter =("fecha",)
    list_filter =("almacen","usuario",)
    date_hierarchy = "fecha"

class PrecioProveedorAdmin(admin.ModelAdmin):
    list_filter=("proveedor",)
    search_fields=("descripcion_proveedor",)
    list_display =("repuesto", "descripcion_proveedor","proveedor",)

class RepuestoAdmin(admin.ModelAdmin):
    search_fields=("nombre",)
    list_display =("id","nombre", "nombre_comun",)
class ProveedorAdmin(admin.ModelAdmin):
    search_fields=("nombre",)
    list_display =("id","nombre",)

admin.site.register(Repuesto, RepuestoAdmin)
admin.site.register(TipoUnidad)
admin.site.register(TipoRepuesto)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Contacto)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(LineaPedido, LineaPedidoAdmin)
admin.site.register(Movimiento, MovimientoAdmin)
admin.site.register(Almacen)
admin.site.register(Inventario)
admin.site.register(LineaInventario)
admin.site.register(StockMinimo, StockMinimoAdmin)
admin.site.register(ContadorPedidos)
admin.site.register(LineaAdicional)
admin.site.register(Entrega)
admin.site.register(Salida)
admin.site.register(LineaSalida)
admin.site.register(PrecioRepuesto, PrecioProveedorAdmin)