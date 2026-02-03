from rest_framework import routers
from django.urls import path
from .views import estado_maquina, nuevo_periodo, generar_anual, actualizar_horario, obtener_anual, guardar_festivos, obtener_codigos, guardar_paradas_agrupadas, leer_paradas_run, obtener_palabraclave, obtener_codigos_resto
from .views import HorarioDiaViewSet, RegistroViewSet, ZonaPerfilVelocidadViewSet, TipoParadaViewSet, DestrezasVelocidadViewSet, ParadaActualizarViewSet, ParadaCrearViewSet, PeriodoViewSet

router = routers.DefaultRouter()
router.register('paradas_crear', ParadaCrearViewSet)
router.register('periodo', PeriodoViewSet)
router.register('paradas', ParadaActualizarViewSet)
router.register('lineas', ZonaPerfilVelocidadViewSet)
router.register('registro', RegistroViewSet)
router.register('horariodia', HorarioDiaViewSet)
router.register('tipoparada', TipoParadaViewSet)
router.register('destrezas_velocidad', DestrezasVelocidadViewSet)

urlpatterns = [
    path('estado/<int:id>/', estado_maquina),
    path('nuevo_periodo/', nuevo_periodo),
    path('obtener_palabraclave/', obtener_palabraclave),
    path('obtener_codigos/', obtener_codigos),
    path('obtener_codigos_resto/', obtener_codigos_resto),
    path('guardar_paradas_agrupadas/', guardar_paradas_agrupadas),
    path('leer_paradas_run/', leer_paradas_run),
    path("horarios/festivos/", guardar_festivos),
    path('horarios/anual/', obtener_anual),
    path('horarios/generar/', generar_anual),
    path('horarios/<str:fecha>/', actualizar_horario), #mejor dejar al final
]
urlpatterns += router.urls