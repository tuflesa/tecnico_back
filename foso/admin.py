from django.contrib import admin
from .models import Linea, Posicion, Bobina, Ocupacion, Material, Proveedor

class LineaAdmin(admin.ModelAdmin):
    list_display  = ('id', 'nombre', 'activa', 'creada_en')
    list_filter   = ('activa',)
    search_fields = ('nombre',)

class PosicionAdmin(admin.ModelAdmin):
    list_display  = ('id', 'linea', 'altura', 'columna')
    list_filter   = ('linea', 'altura')
    search_fields = ('linea__nombre',)

class BobinaAdmin(admin.ModelAdmin):
    list_display  = ('id', 'codigo', 'material', 'peso_kg', 'colada', 'proveedor', 'creada_en')
    list_filter   = ('material', 'proveedor')
    search_fields = ('codigo', 'colada', 'proveedor')

class OcupacionAdmin(admin.ModelAdmin):
    list_display  = ('id', 'bobina', 'posicion', 'activo', 'fecha_inicio', 'fecha_fin')
    list_filter   = ('activo', 'posicion__linea')
    search_fields = ('bobina__codigo',)

class MaterialAdmin(admin.ModelAdmin):
    list_display  = ('id', 'nombre')
    search_fields = ('nombre',)

class ProveedorAdmin(admin.ModelAdmin):
    list_display  = ('id', 'nombre')
    search_fields = ('nombre',)

admin.site.register(Linea, LineaAdmin)
admin.site.register(Posicion, PosicionAdmin)
admin.site.register(Bobina, BobinaAdmin)
admin.site.register(Ocupacion, OcupacionAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Proveedor, ProveedorAdmin)