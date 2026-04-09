from django.contrib import admin
from .models import Foso, Linea, Posicion, Bobina, Ocupacion, Material, Proveedor, DestrezasFoso


class FosoAdmin(admin.ModelAdmin):
    list_display  = ('id', 'empresa', 'nombre', 'activo', 'creado_en')
    list_filter   = ('activo', 'empresa')
    search_fields = ('nombre', 'empresa__nombre')


class LineaAdmin(admin.ModelAdmin):
    list_display  = ('id', 'foso', 'nombre', 'activa', 'creada_en')
    list_filter   = ('activa', 'foso', 'foso__empresa')
    search_fields = ('nombre', 'foso__nombre', 'foso__empresa__nombre')


class PosicionAdmin(admin.ModelAdmin):
    list_display  = ('id', 'linea', 'altura', 'columna', 'habilitada')
    list_filter   = ('linea', 'altura', 'habilitada')
    search_fields = ('linea__nombre', 'linea__foso__nombre')


class BobinaAdmin(admin.ModelAdmin):
    list_display  = ('id', 'codigo', 'material', 'peso_kg', 'colada', 'proveedor', 'creada_en')
    list_filter   = ('material', 'proveedor')
    search_fields = ('codigo', 'colada', 'proveedor__nombre')


class OcupacionAdmin(admin.ModelAdmin):
    list_display  = ('id', 'bobina', 'posicion', 'activo', 'fecha_inicio', 'fecha_fin')
    list_filter   = ('activo', 'posicion__linea', 'posicion__linea__foso')
    search_fields = ('bobina__codigo',)


class MaterialAdmin(admin.ModelAdmin):
    list_display  = ('id', 'nombre')
    search_fields = ('nombre',)


class ProveedorAdmin(admin.ModelAdmin):
    list_display  = ('id', 'nombre')
    search_fields = ('nombre',)


class DestrezasFosoAdmin(admin.ModelAdmin):
    list_display  = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)


admin.site.register(Foso, FosoAdmin)
admin.site.register(Linea, LineaAdmin)
admin.site.register(Posicion, PosicionAdmin)
admin.site.register(Bobina, BobinaAdmin)
admin.site.register(Ocupacion, OcupacionAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(DestrezasFoso, DestrezasFosoAdmin)