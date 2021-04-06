from django.urls import path
from rest_framework import routers
from .views import EstructuraViewSet

router = routers.DefaultRouter()
router.register('estructura', EstructuraViewSet)

urlpatterns = router.urls