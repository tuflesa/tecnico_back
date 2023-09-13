from rest_framework import routers
from .views import RodilloViewSet, PlanoViewSet, RevisionViewSet, SeccionViewSet, OperacionViewSet, TipoRodilloViewSet, MaterialViewSet, GrupoViewSet, TipoPlanoViewSet, Rodillo_listViewSet, Rodillo_editarViewSet
#direcciones de rodillos
router = routers.DefaultRouter()
router.register('grupo_nuevo', GrupoViewSet)
router.register('grupo', GrupoViewSet)
router.register('tipo_plano', TipoPlanoViewSet)
router.register('lista_rodillos', Rodillo_listViewSet)
router.register('rodillo_editar', Rodillo_editarViewSet)
router.register('rodillo_nuevo', RodilloViewSet)
router.register('materiales', MaterialViewSet)
router.register('tipo_rodillo', TipoRodilloViewSet)
router.register('operacion', OperacionViewSet)
router.register('seccion', SeccionViewSet)
#router.register('lista_rodillos', RodilloViewSet)
router.register('crear_plano', PlanoViewSet)
router.register('revision_plano', RevisionViewSet)


urlpatterns = router.urls