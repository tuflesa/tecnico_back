from rest_framework import routers
from .views import NotificacionViewSet, TareaViewSet, EspecialidadViewSet

router = routers.DefaultRouter()
router.register('notificaciones', NotificacionViewSet)
router.register('tareas', TareaViewSet)
router.register('especialidades', EspecialidadViewSet)

urlpatterns = router.urls