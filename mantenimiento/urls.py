from rest_framework import routers
from .views import NotificacionViewSet

router = routers.DefaultRouter()
router.register('notificaciones', NotificacionViewSet)

urlpatterns = router.urls