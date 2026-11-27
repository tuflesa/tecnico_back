from django.contrib import admin
from .models import Agencia, Carga, Bascula, Situacion, Estados, Tipo_carga

class CargaAdmin(admin.ModelAdmin):
    search_fields=("matricula",)
    list_display=("id", "cliente","destino", "matricula")

class SituacionAdmin(admin.ModelAdmin):
    list_display=("id", "nombre_situacion","color")

class TipoAdmin(admin.ModelAdmin):
    list_display=("id", "tipo")

admin.site.register(Carga, CargaAdmin)
admin.site.register(Agencia)
admin.site.register(Bascula)
admin.site.register(Situacion, SituacionAdmin)
admin.site.register(Estados)
admin.site.register(Tipo_carga, TipoAdmin)