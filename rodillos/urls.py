from rest_framework import routers
from .views import RodilloViewSet

router = routers.DefaultRouter()
router.register('lista_rodillos', RodilloViewSet)

urlpatterns = router.urls