from rest_framework import routers
from .views import AgenciaViewSet, CargaListViewSet, CargaViewSet

router = routers.DefaultRouter()

router.register('agencia', AgenciaViewSet)
router.register('lista', CargaListViewSet)
router.register('carga', CargaViewSet)

urlpatterns = router.urls