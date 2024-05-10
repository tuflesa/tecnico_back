from django.contrib import admin

from mantenimiento.models import Especialidad, EstadoLineasTareas, LineaParteTrabajo, Notificacion, ParteTrabajo, Tarea, TipoPeriodo, TipoTarea, TrabajadoresLineaParte, Reclamo

class ParteTrabajoAdmin(admin.ModelAdmin):
    list_filter=("estado",)
    search_fields=("num_parte",)
    list_display=("nombre", "num_parte",)

class LineasTrabajoAdmin(admin.ModelAdmin):
    list_filter=("estado",)
    search_fields=("parte__num_parte",)
    list_display=("tarea", "parte",)

class EspecialidadAdmin(admin.ModelAdmin):
    list_display=("nombre", "id",)

class EstadoAdmin(admin.ModelAdmin):
    list_display=("nombre", "id",)

admin.site.register(Notificacion)
admin.site.register(ParteTrabajo, ParteTrabajoAdmin)
admin.site.register(LineaParteTrabajo, LineasTrabajoAdmin)
admin.site.register(TipoPeriodo)
admin.site.register(TipoTarea)
admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(Tarea)
admin.site.register(EstadoLineasTareas, EstadoAdmin)
admin.site.register(TrabajadoresLineaParte)
admin.site.register(Reclamo)