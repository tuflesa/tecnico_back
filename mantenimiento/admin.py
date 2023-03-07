from django.contrib import admin

from mantenimiento.models import Especialidad, EstadoLineasTareas, LineaParteTrabajo, Notificacion, ParteTrabajo, Tarea, TipoPeriodo, TipoTarea, TrabajadoresLineaParte

class ParteTrabajoAdmin(admin.ModelAdmin):
    list_filter=("estado",)
    search_fields=("num_parte",)

admin.site.register(Notificacion)
admin.site.register(ParteTrabajo, ParteTrabajoAdmin)
admin.site.register(LineaParteTrabajo)
admin.site.register(TipoPeriodo)
admin.site.register(TipoTarea)
admin.site.register(Especialidad)
admin.site.register(Tarea)
admin.site.register(EstadoLineasTareas)
admin.site.register(TrabajadoresLineaParte)