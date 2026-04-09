from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FosoViewSet, LineaViewSet, PosicionViewSet,
    BobinaViewSet, OcupacionViewSet,
    MaterialViewSet, ProveedorViewSet
)

router = DefaultRouter()
router.register(r"fosos",      FosoViewSet)
router.register(r"lineas",     LineaViewSet)
router.register(r"posiciones", PosicionViewSet)
router.register(r"bobinas",    BobinaViewSet)
router.register(r"ocupaciones", OcupacionViewSet)
router.register(r"materiales",  MaterialViewSet)
router.register(r"proveedores", ProveedorViewSet)

urlpatterns = [
    path("", include(router.urls)),
]