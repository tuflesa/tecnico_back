from rest_framework import routers
from .views import RegistroViewSet, ZonaPerfilVelocidadViewSet

router = routers.DefaultRouter()
router.register('lineas', ZonaPerfilVelocidadViewSet)
router.register('registro', RegistroViewSet)

urlpatterns = router.urls