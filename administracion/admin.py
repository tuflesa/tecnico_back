from django.contrib import admin
from .models import Aplicacion, Perfil, Puesto, NivelAcceso

admin.site.register(Aplicacion)
admin.site.register(NivelAcceso)
admin.site.register(Perfil)
admin.site.register(Puesto)