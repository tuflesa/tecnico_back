from rest_framework import routers
from .views import RodilloViewSet, PlanoViewSet, RevisionViewSet, SeccionViewSet, OperacionViewSet, TipoRodilloViewSet, MaterialViewSet, GrupoViewSet

router = routers.DefaultRouter()
router.register('rodillo_nuevo', RodilloViewSet)
router.register('grupo', GrupoViewSet)
router.register('materiales', MaterialViewSet)
router.register('tipo_rodillo', TipoRodilloViewSet)
router.register('operacion', OperacionViewSet)
router.register('seccion', SeccionViewSet)
router.register('lista_rodillos', RodilloViewSet)
router.register('crear_plano', PlanoViewSet)
router.register('revision_plano', RevisionViewSet)


urlpatterns = router.urls