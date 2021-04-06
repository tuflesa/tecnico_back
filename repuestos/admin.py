from django.contrib import admin
from .models import Repuesto, Proveedor, Contacto, Pedido, LineaPedido, Movimiento

admin.site.register(Repuesto)
admin.site.register(Proveedor)
admin.site.register(Contacto)
admin.site.register(Pedido)
admin.site.register(LineaPedido)
admin.site.register(Movimiento)
