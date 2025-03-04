from django.contrib import admin
from .models import Direcciones, Empresa, Zona, Seccion, Equipo

class ZonaAdmin(admin.ModelAdmin):
    search_fields=("siglas",)
    list_display=("id","nombre", "siglas", "empresa")

admin.site.register(Empresa)
admin.site.register(Zona, ZonaAdmin)
admin.site.register(Seccion)
admin.site.register(Equipo)
admin.site.register(Direcciones)