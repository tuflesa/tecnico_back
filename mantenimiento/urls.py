from rest_framework import routers
from .views import NotificacionViewSet, TareaViewSet, EspecialidadViewSet, TipoTareaViewSet, TipoPeriodoViewSet, TareaNuevaViewSet, ParteTrabajoViewSet

router = routers.DefaultRouter()
router.register('parte_trabajo', ParteTrabajoViewSet)
router.register('tarea_nueva', TareaNuevaViewSet)
router.register('notificaciones', NotificacionViewSet)
router.register('tareas', TareaViewSet)
router.register('especialidades', EspecialidadViewSet)
router.register('tipo_tarea', TipoTareaViewSet)
router.register('tipo_periodo', TipoPeriodoViewSet)

urlpatterns = router.urls