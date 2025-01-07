from django.urls import path
from .views import EjesViewSet, PCViewSet, DiametrosActPLC, PosicionesActPLC

urlpatterns = [
    path('ejes/', EjesViewSet.as_view()),
    path('pc/', PCViewSet.as_view()),
    path('diametros_actuales_PLC/', DiametrosActPLC.as_view()),
    path('posiciones_actuales_PLC/', PosicionesActPLC.as_view())
]