from rest_framework import routers
from .views import RodilloViewSet, PlanoNuevoViewSet, RevisionViewSet, SeccionViewSet, OperacionViewSet, TipoRodilloViewSet, MaterialViewSet, GrupoViewSet, TipoPlanoViewSet, Rodillo_listViewSet, Rodillo_editarViewSet, PlanoParametrosViewSet, Nombres_ParametrosViewSet, TipoSeccionViewSet, PlanoViewSet, RevisionConjuntosViewSet, Parametros_estandarViewSet, Plano_existenteViewSet, EjeViewSet, BancadaViewSet, ConjuntoViewSet, ElementoViewSet, Elemento_SelectViewSet, BancadaGruposViewSet, CeldaViewSet, Celda_SelectViewSet, Rodillo_existenteViewSet, Grupo_onlyViewSet, Operacion_CTViewSet, FormaViewSet, Celda_DuplicarViewSet, BancadaCTViewSet, Grupo_NuevoViewSet
#direcciones de rodillos
router = routers.DefaultRouter()
router.register('grupo_nuevo', Grupo_NuevoViewSet)
router.register('bancada_ct', BancadaCTViewSet)
router.register('forma', FormaViewSet)
router.register('operacion_ct', Operacion_CTViewSet)
router.register('grupo_only', Grupo_onlyViewSet)
router.register('celda_duplicar', Celda_DuplicarViewSet)
router.register('celda_select', Celda_SelectViewSet)
router.register('rodillos_existentes', Rodillo_existenteViewSet)
router.register('celda', CeldaViewSet)
router.register('plano', PlanoViewSet)
router.register('bancada_grupos', BancadaGruposViewSet)
router.register('elemento_select', Elemento_SelectViewSet)
router.register('bancada', BancadaViewSet)
router.register('elemento', ElementoViewSet)
router.register('conjunto', ConjuntoViewSet)
router.register('eje', EjeViewSet)
router.register('planos_existentes', Plano_existenteViewSet)
router.register('parametros_estandar', Parametros_estandarViewSet)
router.register('nombres_parametros', Nombres_ParametrosViewSet)
router.register('revision_conjuntos', RevisionConjuntosViewSet)
router.register('plano_nuevo', PlanoNuevoViewSet)
router.register('grupo', GrupoViewSet)
router.register('tipo_plano', TipoPlanoViewSet)
router.register('plano_parametros', PlanoParametrosViewSet) #para sacar los nombres de los parametros que pertenecen a un tipo de plano
router.register('lista_rodillos', Rodillo_listViewSet)
router.register('rodillo_editar', Rodillo_editarViewSet)
router.register('rodillo_nuevo', RodilloViewSet)
router.register('materiales', MaterialViewSet)
router.register('tipo_rodillo', TipoRodilloViewSet)
router.register('operacion', OperacionViewSet)
router.register('seccion', SeccionViewSet)
router.register('revision_plano', RevisionViewSet)
router.register('tipo_seccion', TipoSeccionViewSet)

urlpatterns = router.urls