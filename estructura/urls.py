# from django.urls import path
from rest_framework import routers
from .views import  DireccionesEmpresaViewSet, EmpresaViewSet, ZonaViewSet, SeccionViewSet, EquipoViewSet

router = routers.DefaultRouter()
router.register('empresa', EmpresaViewSet)
router.register('zona', ZonaViewSet)
router.register('seccion', SeccionViewSet)
router.register('equipo', EquipoViewSet)
router. register('direcciones', DireccionesEmpresaViewSet)

urlpatterns = router.urls