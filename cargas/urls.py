from rest_framework import routers
from .views import AgenciaViewSet, CargaListViewSet, CargaViewSet, BasculaViewSet

router = routers.DefaultRouter()

router.register('agencia', AgenciaViewSet)
router.register('lista', CargaListViewSet)
router.register('carga', CargaViewSet)
router.register('bascula', BasculaViewSet)

urlpatterns = router.urls