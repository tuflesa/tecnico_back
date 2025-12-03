from rest_framework import routers
from django.urls import path
from .views import RegistroViewSet, ZonaPerfilVelocidadViewSet, estado_maquina, nuevo_periodo

router = routers.DefaultRouter()
router.register('lineas', ZonaPerfilVelocidadViewSet)
router.register('registro', RegistroViewSet)

urlpatterns = [
    path('estado/<int:id>/', estado_maquina),
    path('nuevo_periodo/', nuevo_periodo),
]
urlpatterns += router.urls