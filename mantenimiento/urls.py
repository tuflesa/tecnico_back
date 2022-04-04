from rest_framework import routers
from .views import NotificacionViewSet, TareaViewSet, EspecialidadViewSet, TipoTareaViewSet, TipoPeriodoViewSet, TareaNuevaViewSet, ParteTrabajoViewSet, ParteTrabajoDetalleViewSet, LineaParteTrabajoViewSet, LineaParteTrabajoNuevaViewSet, LineaParteTrabajoMovViewSet, ListadoLineaParteViewSet, EstadoLineasTareasViewSet

router = routers.DefaultRouter()
router.register('estados', EstadoLineasTareasViewSet)
router.register('linea_nueva', LineaParteTrabajoNuevaViewSet)
router.register('lineas_parte_trabajo', LineaParteTrabajoViewSet)
router.register('listado_lineas_partes', ListadoLineaParteViewSet)
router.register('parte_trabajo_detalle', ParteTrabajoDetalleViewSet)
router.register('parte_trabajo', ParteTrabajoViewSet)
router.register('lineas_parte_mov', LineaParteTrabajoMovViewSet)
router.register('tarea_nueva', TareaNuevaViewSet)
router.register('notificaciones', NotificacionViewSet)
router.register('tareas', TareaViewSet)
router.register('especialidades', EspecialidadViewSet)
router.register('tipo_tarea', TipoTareaViewSet)
router.register('tipo_periodo', TipoPeriodoViewSet)

urlpatterns = router.urls