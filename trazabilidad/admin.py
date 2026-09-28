from django.contrib import admin
from .models import Acumulador, Flejes, Tubos, OF, Forma, Montaje

class OFAdmin(admin.ModelAdmin):
    list_filter=("zona",)
    search_fields=("numero",)
    list_display =("numero", "inicio","fin",)

class MontajeAdmin(admin.ModelAdmin):
    list_filter=("of__zona__siglas",)
    list_display =("of", "inicio","fin","of",)

class FlejeAdmin(admin.ModelAdmin):
    list_filter=("maquina_siglas",)

admin.site.register(Acumulador)
admin.site.register(Flejes, FlejeAdmin)
admin.site.register(Tubos)
admin.site.register(OF, OFAdmin)
admin.site.register(Forma)
admin.site.register(Montaje, MontajeAdmin)