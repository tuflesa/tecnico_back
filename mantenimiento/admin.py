from django.contrib import admin

from .models import Especialidad, EstadoLineasTareas, LineaParteTrabajo, Notificacion, ParteTrabajo, Tarea, TipoPeriodo, TipoTarea, TrabajadoresLineaParte

admin.site.register(Notificacion)
admin.site.register(ParteTrabajo)
admin.site.register(LineaParteTrabajo)
admin.site.register(TipoPeriodo)
admin.site.register(TipoTarea)
admin.site.register(Especialidad)
admin.site.register(Tarea)
admin.site.register(EstadoLineasTareas)
admin.site.register(TrabajadoresLineaParte)