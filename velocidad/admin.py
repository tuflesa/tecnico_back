from django.contrib import admin
from .models import ZonaPerfilVelocidad, Registro, TipoParada, CodigoParada, Parada, Periodo, HorarioDia, DestrezasVelocidad

class ParadasAdmin(admin.ModelAdmin):
    # Añadimos los métodos al list_display
    list_display = ("id", "codigo", "get_inicio", "get_fin", "get_duracion")
    list_filter = ("zona", "codigo")
    search_fields = ("zona__nombre", "codigo__nombre", "periodos__inicio")

    # Definimos métodos "puente" para personalizar las etiquetas en el Admin
    def get_inicio(self, obj):
        return obj.inicio()
    get_inicio.short_description = 'Inicio' # Título de la columna

    def get_fin(self, obj):
        return obj.fin()
    get_fin.short_description = 'Fin'

    def get_duracion(self, obj):
        # Mostramos 2 decimales para que se vea limpio
        return f"{obj.duracion():.2f} min"
    get_duracion.short_description = 'Duración (min)'

class HorarioDiaAdmin(admin.ModelAdmin):
    list_filter=("zona",)
    search_fields=("fecha",)

admin.site.register(ZonaPerfilVelocidad)
admin.site.register(Registro)
admin.site.register(DestrezasVelocidad)
admin.site.register(TipoParada)
admin.site.register(CodigoParada)
admin.site.register(Parada, ParadasAdmin)
admin.site.register(Periodo)
admin.site.register(HorarioDia, HorarioDiaAdmin)
# admin.site.register(Registro, RegistroAdmin)
