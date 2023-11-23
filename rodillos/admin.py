from django.contrib import admin
from .models import Tipo_Seccion, Seccion, Operacion, Eje, Rodillo, Tipo_rodillo, Material, Bancada, Conjunto, Elemento, Grupo, Montaje, Plano, Revision, Tipo_Plano, Nombres_Parametros, Instancia, Parametros_Estandar, Parametros, Celda

class RevisionAdmin(admin.ModelAdmin):
    search_fields=("plano__nombre",)
    list_display=("id","plano", "motivo", "fecha",)
    list_filter=("motivo",)

class MaterialAdmin(admin.ModelAdmin):
    search_fields=("nombre",)

class OperacionAdmin(admin.ModelAdmin):
    search_fields=("seccion__maquina__siglas",)
    list_display=("id","nombre", "seccion",)
    list_filter=("seccion__nombre",)

class ParametrosAdmin(admin.ModelAdmin):
    search_fields=("revision__plano__nombre",)
    list_display=("id","nombre", "valor",)
    list_filter=("nombre",)

class PlanosAdmin(admin.ModelAdmin):
    search_fields=("nombre",)
    list_display=("id","nombre",)
    list_filter=("rodillos",)

class RodillosAdmin(admin.ModelAdmin):
    search_fields=("nombre",)
    list_display=("id","nombre", "grupo", "tipo")
    list_filter=("grupo", "tipo",)

class TipoPlanoAdmin(admin.ModelAdmin):
    search_fields=("nombre",)
    list_display=("id","nombre")

class EjeAdmin(admin.ModelAdmin):
    search_fields=("diametro",)
    list_filter=("tipo", "operacion")

class Tipo_SeccionAdmin(admin.ModelAdmin):
    search_fields=("nombre",)
    list_display=("id","nombre")

class GrupoAdmin(admin.ModelAdmin):
    list_display=("id","nombre")

admin.site.register(Tipo_Seccion, Tipo_SeccionAdmin)
admin.site.register(Seccion)
admin.site.register(Operacion, OperacionAdmin)
admin.site.register(Eje, EjeAdmin)
admin.site.register(Rodillo, RodillosAdmin)
admin.site.register(Tipo_rodillo)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Bancada)
admin.site.register(Conjunto)
admin.site.register(Elemento)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Montaje)
admin.site.register(Plano, PlanosAdmin)
admin.site.register(Revision, RevisionAdmin)
admin.site.register(Tipo_Plano, TipoPlanoAdmin)
admin.site.register(Nombres_Parametros)
admin.site.register(Instancia)
admin.site.register(Parametros_Estandar)
admin.site.register(Parametros, ParametrosAdmin)
admin.site.register(Celda)