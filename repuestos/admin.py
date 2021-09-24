from django.contrib import admin
from .models import Repuesto, Proveedor, Contacto, Pedido, LineaPedido, Movimiento, Almacen, Inventario, LineaInventario, StockMinimo, TipoRepuesto

admin.site.register(Repuesto)
admin.site.register(TipoRepuesto)
admin.site.register(Proveedor)
admin.site.register(Contacto)
admin.site.register(Pedido)
admin.site.register(LineaPedido)
admin.site.register(Movimiento)
admin.site.register(Almacen)
admin.site.register(Inventario)
admin.site.register(LineaInventario)
admin.site.register(StockMinimo)