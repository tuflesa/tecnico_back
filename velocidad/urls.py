from rest_framework import routers
from django.urls import path
from .views import estado_maquina, nuevo_periodo, generar_anual, actualizar_horario, obtener_anual, guardar_festivos, obtener_codigos
from .views import HorarioDiaViewSet, RegistroViewSet, ZonaPerfilVelocidadViewSet, TipoParadaViewSet

router = routers.DefaultRouter()
router.register('lineas', ZonaPerfilVelocidadViewSet)
router.register('registro', RegistroViewSet)
router.register('horariodia', HorarioDiaViewSet)
router.register('tipoparada', TipoParadaViewSet)

urlpatterns = [
    path('estado/<int:id>/', estado_maquina),
    path('nuevo_periodo/', nuevo_periodo),
    path("horarios/festivos/", guardar_festivos),
    path('horarios/anual/', obtener_anual),
    path('horarios/generar/', generar_anual),
    path('obtener_codigos/', obtener_codigos),
    path('horarios/<str:fecha>/', actualizar_horario),
]
urlpatterns += router.urls