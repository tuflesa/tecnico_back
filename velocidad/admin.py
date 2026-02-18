from django.contrib import admin
from .models import ZonaPerfilVelocidad, Registro, TipoParada, CodigoParada, Parada, Periodo, HorarioDia, DestrezasVelocidad, PalabrasClave, Turnos

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
    list_display =("id","fecha", "zona", "turno_mañana",)

class CodigoParadaAdmin(admin.ModelAdmin):
    list_filter=("palabra_clave","zona", "tipo")

class PeriodoAdmin(admin.ModelAdmin):
    list_display =("id","parada", "inicio", "fin", "velocidad",)
    search_fields=("parada__id",)

class DestrezasAdmin(admin.ModelAdmin):
    list_display =("id","nombre", "descripcion",)
    search_fields=("nombre",)

class TurnosAdmin(admin.ModelAdmin):
    list_display =("id", "display_turno", "zona",)
    list_filter=("activo","zona")
    
    def display_turno(self, obj):
            return str(obj)
    display_turno.short_description = "Turno"


admin.site.register(ZonaPerfilVelocidad)
admin.site.register(Turnos, TurnosAdmin)
admin.site.register(Registro)
admin.site.register(DestrezasVelocidad, DestrezasAdmin)
admin.site.register(TipoParada)
admin.site.register(CodigoParada, CodigoParadaAdmin)
admin.site.register(PalabrasClave)
admin.site.register(Parada, ParadasAdmin)
admin.site.register(Periodo, PeriodoAdmin)
admin.site.register(HorarioDia, HorarioDiaAdmin)
# admin.site.register(Registro, RegistroAdmin)
