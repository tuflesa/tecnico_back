from rest_framework import routers
from .views import ArticuloViewSet

router = routers.DefaultRouter()

router.register('articulos', ArticuloViewSet)

urlpatterns = router.urls