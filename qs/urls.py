from django.urls import path
from .views import EjesViewSet, PCViewSet, ArticuloViewSet


urlpatterns = [
    path('ejes/', EjesViewSet.as_view()),
    path('pc/', PCViewSet.as_view()),
    path('articulos/', ArticuloViewSet)
]