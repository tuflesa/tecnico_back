from django.contrib import admin
from .models import Agencia, Carga, Bascula, Situacion, Estados, Tipo_carga

admin.site.register(Carga)
admin.site.register(Agencia)
admin.site.register(Bascula)
admin.site.register(Situacion)
admin.site.register(Estados)
admin.site.register(Tipo_carga)