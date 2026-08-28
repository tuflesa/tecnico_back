from rest_framework import routers
from .views import ArticuloViewSet, FormasViewSet, AcabadoViewSet, NormaViewSet, CalidadViewSet

router = routers.DefaultRouter()

router.register('articulos', ArticuloViewSet)
router.register('norma', NormaViewSet)
router.register('acabado', AcabadoViewSet)
router.register('calidad', CalidadViewSet)
router.register('formas', FormasViewSet)

urlpatterns = router.urls