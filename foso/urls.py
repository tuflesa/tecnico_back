from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LineaViewSet, PosicionViewSet, BobinaViewSet, OcupacionViewSet

router = DefaultRouter()
router.register(r"lineas",     LineaViewSet)
router.register(r"posiciones", PosicionViewSet)
router.register(r"bobinas",    BobinaViewSet)
router.register(r"ocupaciones", OcupacionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]