from django.contrib import admin

from .models import Especialidad, LineaParteTrabajo, Notificacion, ParteTrabajo, Tarea, TipoPeriodo, TipoTarea

admin.site.register(Notificacion)
admin.site.register(ParteTrabajo)
admin.site.register(LineaParteTrabajo)
admin.site.register(TipoPeriodo)
admin.site.register(TipoTarea)
admin.site.register(Especialidad)
admin.site.register(Tarea)