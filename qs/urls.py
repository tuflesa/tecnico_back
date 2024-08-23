from django.urls import path
from .views import EjesViewSet, PCViewSet


urlpatterns = [
    path('ejes/', EjesViewSet.as_view()),
    path('pc/', PCViewSet.as_view())
]