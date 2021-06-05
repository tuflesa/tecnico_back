from django.contrib import admin
from .models import Agencia, Carga, Bascula

admin.site.register(Carga)
admin.site.register(Agencia)
admin.site.register(Bascula)