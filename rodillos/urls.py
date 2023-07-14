from rest_framework import routers
from .views import RodilloViewSet, PlanoViewSet, RevisionViewSet

router = routers.DefaultRouter()
router.register('lista_rodillos', RodilloViewSet)
router.register('crear_plano', PlanoViewSet)
router.register('revision_plano', RevisionViewSet)

urlpatterns = router.urls