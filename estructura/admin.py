from django.contrib import admin
from .models import Direcciones, Empresa, Zona, Seccion, Equipo

class ZonaAdmin(admin.ModelAdmin):
    search_fields=("siglas",)
    list_display=("id","nombre", "siglas", "empresa")
    list_filter=("empresa",)

class SeccionAdmin(admin.ModelAdmin):
    search_fields=("zona__nombre",)
    list_display=("id","nombre", "zona")
    list_filter=("zona__empresa",)

class EquipoAdmin(admin.ModelAdmin):
    search_fields=("seccion__nombre",)
    list_display=("id","nombre", "seccion")

admin.site.register(Empresa)
admin.site.register(Zona, ZonaAdmin)
admin.site.register(Seccion, SeccionAdmin)
admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Direcciones)