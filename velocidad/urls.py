from rest_framework import routers
from django.urls import path
from .views import RegistroViewSet, ZonaPerfilVelocidadViewSet, estado_maquina

router = routers.DefaultRouter()
router.register('lineas', ZonaPerfilVelocidadViewSet)
router.register('registro', RegistroViewSet)

urlpatterns = [
    path('estado/<int:id>/', estado_maquina),
]
urlpatterns += router.urls