from rest_framework import routers
from .views import RodilloViewSet, PlanoViewSet, RevisionViewSet, SeccionViewSet, OperacionViewSet, TipoRodilloViewSet, MaterialViewSet, GrupoViewSet, TipoPlanoViewSet, Tipo_rodilloViewSet

router = routers.DefaultRouter()
router.register('grupo_nuevo', GrupoViewSet)
router.register('tipo_plano', TipoPlanoViewSet)
router.register('rodillo_nuevo', RodilloViewSet)
router.register('materiales', MaterialViewSet)
router.register('tipo_rodillo', TipoRodilloViewSet)
router.register('operacion', OperacionViewSet)
router.register('seccion', SeccionViewSet)
router.register('lista_rodillos', RodilloViewSet)
router.register('crear_plano', PlanoViewSet)
router.register('revision_plano', RevisionViewSet)
router.register('tipo_plano', TipoPlanoViewSet)
router.register('seccion', SeccionViewSet)
router.register('operacion', OperacionViewSet)
router.register('tipo_rodillo', Tipo_rodilloViewSet)
router.register('materiales', MaterialViewSet)



urlpatterns = router.urls