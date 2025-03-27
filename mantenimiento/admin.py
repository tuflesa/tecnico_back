from django.contrib import admin

from mantenimiento.models import Especialidad, EstadoLineasTareas, LineaParteTrabajo, Notificacion, ParteTrabajo, Tarea, TipoPeriodo, TipoTarea, TrabajadoresLineaParte, Reclamo

class ParteTrabajoAdmin(admin.ModelAdmin):
    list_filter=("estado",)
    search_fields=("num_parte",)
    list_display=("id","nombre", "num_parte",)

class LineasTrabajoAdmin(admin.ModelAdmin):
    list_filter=("estado",)
    search_fields=("parte__num_parte",)
    list_display=("id","tarea", "parte",)
class TrabajadorLineasAdmin(admin.ModelAdmin):
    list_filter=("trabajador",)
    search_fields=("linea__parte__num_parte",)
    list_display=("id", "trabajador","linea",)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display=("nombre", "id",)

class EstadoAdmin(admin.ModelAdmin):
    list_display=("nombre", "id",)
class TareasAdmin(admin.ModelAdmin):
    list_display=("id","nombre",)
    search_fields=("nombre",)

admin.site.register(Notificacion)
admin.site.register(ParteTrabajo, ParteTrabajoAdmin)
admin.site.register(LineaParteTrabajo, LineasTrabajoAdmin)
admin.site.register(TipoPeriodo)
admin.site.register(TipoTarea)
admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(Tarea, TareasAdmin)
admin.site.register(EstadoLineasTareas, EstadoAdmin)
admin.site.register(TrabajadoresLineaParte, TrabajadorLineasAdmin)
admin.site.register(Reclamo)