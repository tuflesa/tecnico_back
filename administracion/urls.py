from django.urls import path
from rest_framework import routers
from .views import AplicacionViewSet, UserViewSet

router = routers.DefaultRouter()

router.register('roles', AplicacionViewSet)
router.register('usuarios', UserViewSet)

urlpatterns = router.urls