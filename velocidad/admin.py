from django.contrib import admin
from .models import ZonaPerfilVelocidad, Registro, TipoParada, CodigoParada, Parada, Periodo

class RegistroAdmin(admin.ModelAdmin):
    #search_fields=("zona",)
    #list_display=("zona",)
    list_filter=("zona",)

admin.site.register(ZonaPerfilVelocidad)
<<<<<<< HEAD
admin.site.register(Registro)
admin.site.register(TipoParada)
admin.site.register(CodigoParada)
admin.site.register(Parada)
admin.site.register(Periodo)
=======
admin.site.register(Registro, RegistroAdmin)
>>>>>>> c6ff75713415fee56c9eca74967fe2ffdef61e43
