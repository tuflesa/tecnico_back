from rest_framework import routers
from .views import RodilloViewSet, PlanoViewSet, RevisionViewSet, TipoPlanoViewSet, SeccionViewSet, OperacionViewSet, Tipo_rodilloViewSet, GrupoViewSet, MaterialViewSet

router = routers.DefaultRouter()
router.register('grupos', GrupoViewSet)
router.register('lista_rodillos', RodilloViewSet)
router.register('crear_plano', PlanoViewSet)
router.register('revision_plano', RevisionViewSet)
router.register('tipo_plano', TipoPlanoViewSet)
router.register('seccion', SeccionViewSet)
router.register('operacion', OperacionViewSet)
router.register('tipo_rodillo', Tipo_rodilloViewSet)
router.register('materiales', MaterialViewSet)


urlpatterns = router.urls