from django.contrib import admin
from .models import Aplicacion, Perfil, Puesto, NivelAcceso

class PerfilAdmin(admin.ModelAdmin):
    search_fields=("usuario",)
    list_display=("id","usuario","empresa",)
    list_filter=("empresa","puesto",)

admin.site.register(Aplicacion)
admin.site.register(NivelAcceso)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Puesto)