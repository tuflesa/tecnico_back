from django.urls import path
from rest_framework import routers
from .views import EjesViewSet, PCViewSet, DiametrosActPLC, PosicionesActPLC, VarianteViewSet
from .qs import enviarVariantePLC

router = routers.DefaultRouter()

router.register('variante', VarianteViewSet)

urlpatterns = [
    path('ejes/', EjesViewSet.as_view()),
    path('pc/', PCViewSet.as_view()),
    path('diametros_actuales_PLC/', DiametrosActPLC.as_view()),
    path('posiciones_actuales_PLC/', PosicionesActPLC.as_view()),
    path('enviar_variante_PLC/', enviarVariantePLC)
] + router.urls