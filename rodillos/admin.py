from django.contrib import admin
from .models import Tipo_Seccion, Seccion, Operacion, Eje, Rodillo, Tipo_rodillo, Material, Bancada, Conjunto, Elemento, Grupo, Montaje, Plano, Revision, Tipo_Plano, Nombres_Parametros, Instancia, Parametros_Estandar, Parametros, Celda, Forma, Icono, Rectificacion, LineaRectificacion, Posicion, Icono_celda, Anotaciones

class RevisionAdmin(admin.ModelAdmin):
    search_fields=("plano__nombre",)
    list_display=("id","plano", "motivo", "fecha",)
    list_filter=("motivo",)

class MaterialAdmin(admin.ModelAdmin):
    search_fields=("nombre",)

class OperacionAdmin(admin.ModelAdmin):
    search_fields=("seccion__maquina__siglas",)
    list_display=("id","nombre", "seccion",)
    list_filter=("seccion__nombre","seccion__maquina__siglas",)

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
    list_filter=("tipo", "numero_ejes")

class Tipo_SeccionAdmin(admin.ModelAdmin):
    search_fields=("nombre",)
    list_display=("id","nombre")

class ElementoAdmin(admin.ModelAdmin):
    search_fields=("id",)
    list_display=("id","conjunto", "eje", "rodillo")
    list_filter=("eje", "rodillo")

class GrupoAdmin(admin.ModelAdmin):
    list_display=("id","nombre", "maquina")

class SeccionAdmin(admin.ModelAdmin):
    list_display=("id","nombre")

class CeldaAdmin(admin.ModelAdmin):
    list_display=("id","bancada", "conjunto", "operacion")

class ConjuntoAdmin(admin.ModelAdmin):
    list_display=("id","operacion", "tubo_madre")
    search_fields=("tubo_madre",)

class BancadaAdmin(admin.ModelAdmin):
    list_display=("id","seccion", "tubo_madre", "dimensiones", "espesores")
    search_fields=("tubo_madre",)

class MontajesAdmin(admin.ModelAdmin):
    list_display=("id","nombre", "grupo")
    search_fields=("nombre",)

class IconoAdmin(admin.ModelAdmin):
    list_display=("id","nombre")
    search_fields=("nombre",)

class Icono_celdaAdmin(admin.ModelAdmin):
    list_display=("id","nombre")
    search_fields=("nombre",)

class AnotaconesAdmin(admin.ModelAdmin):
    list_display=("id","descripcion", "montaje")
    search_fields=("descripcion",)

class RectificacionAdmin(admin.ModelAdmin):
    list_display=("id","numero", "creado_por")
    search_fields=("numero",)

class LineaRectificacionAdmin(admin.ModelAdmin):
    list_display=("id","rectificado", "instancia")
    search_fields=("id",)

admin.site.register(Tipo_Seccion, Tipo_SeccionAdmin)
admin.site.register(Anotaciones)
admin.site.register(Icono, IconoAdmin)
admin.site.register(Icono_celda, Icono_celdaAdmin)
admin.site.register(Rectificacion, RectificacionAdmin)
admin.site.register(Seccion, SeccionAdmin)
admin.site.register(Operacion, OperacionAdmin)
admin.site.register(Eje, EjeAdmin)
admin.site.register(Rodillo, RodillosAdmin)
admin.site.register(Tipo_rodillo)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Bancada, BancadaAdmin)
admin.site.register(Conjunto, ConjuntoAdmin)
admin.site.register(Elemento, ElementoAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Montaje, MontajesAdmin)
admin.site.register(Plano, PlanosAdmin)
admin.site.register(Revision, RevisionAdmin)
admin.site.register(Tipo_Plano, TipoPlanoAdmin)
admin.site.register(Nombres_Parametros)
admin.site.register(Instancia)
admin.site.register(Parametros_Estandar)
admin.site.register(Parametros, ParametrosAdmin)
admin.site.register(Celda, CeldaAdmin)
admin.site.register(Forma)
admin.site.register(LineaRectificacion, LineaRectificacionAdmin)
admin.site.register(Posicion)