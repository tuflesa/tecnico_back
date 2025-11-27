from django.contrib import admin
from .models import ZonaPerfilVelocidad, Registro

class RegistroAdmin(admin.ModelAdmin):
    #search_fields=("zona",)
    #list_display=("zona",)
    list_filter=("zona",)

admin.site.register(ZonaPerfilVelocidad)
admin.site.register(Registro, RegistroAdmin)
