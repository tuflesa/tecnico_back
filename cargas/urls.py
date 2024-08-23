from rest_framework import routers
from .views import AgenciaViewSet, CargaListViewSet, CargaViewSet, BasculaViewSet, LlamadaViewSet, UltimasLlamadasViewSet

router = routers.DefaultRouter()

router.register('agencia', AgenciaViewSet)
router.register('lista', CargaListViewSet)
router.register('carga', CargaViewSet)
router.register('bascula', BasculaViewSet)
router.register('llamada', LlamadaViewSet)
router.register('ultimas_llamadas', UltimasLlamadasViewSet)

urlpatterns = router.urls