from django.urls import path
from .views import EjesViewSet


urlpatterns = [
    path('ejes/', EjesViewSet.as_view())
]