from rest_framework import routers
from .views import GruposViewSet, ConjuntoViewSet

router = routers.DefaultRouter()
router.register('lista_grupos', GruposViewSet)
router.register('conjuntos', ConjuntoViewSet)

urlpatterns = router.urls