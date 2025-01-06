from django.urls import path
from .views import EjesViewSet, PCViewSet, DiametrosActPLC

urlpatterns = [
    path('ejes/', EjesViewSet.as_view()),
    path('pc/', PCViewSet.as_view()),
    path('diametros_actuales_PLC/', DiametrosActPLC.as_view())
]