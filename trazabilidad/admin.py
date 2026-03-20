from django.contrib import admin
from .models import Acumulador, Flejes, Tubos, OF, Forma, Montaje

class OFAdmin(admin.ModelAdmin):
    list_filter=("zona",)
    search_fields=("numero",)
    list_display =("numero", "inicio","fin",)

admin.site.register(Acumulador)
admin.site.register(Flejes)
admin.site.register(Tubos)
admin.site.register(OF, OFAdmin)
admin.site.register(Forma)
admin.site.register(Montaje)