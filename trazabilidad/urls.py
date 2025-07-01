from django.urls import path
from .trazabilidad import leerFlejesEnAcumuladores, resetPLC, leerEstadoPLC
from rest_framework import routers
from .views import AcumuladorViewSet, FlejesProduccionDB, FlejesViewSet, FlejesListViewSet

router = routers.DefaultRouter()

router.register('acumuladores', AcumuladorViewSet)
router.register('flejes', FlejesViewSet)
router.register('flejesLista', FlejesListViewSet)

urlpatterns = [
    path('leerFlejes/', leerFlejesEnAcumuladores),
    path('resetPLC/', resetPLC),
    path('leerFlejesProduccionDB/', FlejesProduccionDB.as_view()),
    path('leerEstadoPLC/', leerEstadoPLC),
] + router.urls