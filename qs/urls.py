from django.urls import path
from .views import EjesViewSet, PCViewSet, ArticuloViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('articulos', ArticuloViewSet)

urlpatterns = router.urls + [
    path('ejes/', EjesViewSet.as_view()),
    path('pc/', PCViewSet.as_view()),
]