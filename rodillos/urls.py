from rest_framework import routers
from .views import RodilloViewSet, PlanoNuevoViewSet, RevisionViewSet, SeccionViewSet, OperacionViewSet, TipoRodilloViewSet, MaterialViewSet, GrupoViewSet, TipoPlanoViewSet, Rodillo_listViewSet, Rodillo_editarViewSet, PlanoParametrosViewSet, Nombres_ParametrosViewSet, TipoSeccionViewSet, PlanoViewSet, RevisionConjuntosViewSet, ParametrosViewSet
#direcciones de rodillos
router = routers.DefaultRouter()
router.register('grupo_nuevo', GrupoViewSet)
router.register('parametros', ParametrosViewSet)
router.register('nombres_parametros', Nombres_ParametrosViewSet)
router.register('revision_conjuntos', RevisionConjuntosViewSet)
router.register('plano_nuevo', PlanoNuevoViewSet)
router.register('plano', PlanoViewSet)
router.register('grupo', GrupoViewSet)
router.register('tipo_plano', TipoPlanoViewSet)
router.register('plano_parametros', PlanoParametrosViewSet)
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