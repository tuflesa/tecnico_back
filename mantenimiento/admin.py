from django.contrib import admin

from .models import LineaParteTrabajo, Notificacion, ParteTrabajo

admin.site.register(Notificacion)
admin.site.register(ParteTrabajo)
admin.site.register(LineaParteTrabajo)