from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters import rest_framework as filters
from django_filters import BooleanFilter
from distutils.util import strtobool
from .serializers import AcumuladorSerializer, FlejesSimpleSerializer, FlejesSerializer
from .models import Acumulador, Flejes
from .trazabilidad import leerFlejesProduccionDB, leerEstadoPLC

class AcumuladorFilter(filters.FilterSet):
    class Meta:
        model = Acumulador
        fields = {
            'zona__empresa__id': ['exact'],
        }

class FlejesFilter(filters.FilterSet):
    finalizada = BooleanFilter(field_name='finalizada')
    class Meta:
        model = Flejes
        fields = {
            'acumulador': ['exact'],
            'of': ['exact'],
            'finalizada': ['exact']
        }

class AcumuladorViewSet(viewsets.ModelViewSet):
    serializer_class = AcumuladorSerializer
    queryset = Acumulador.objects.all()
    filterset_class = AcumuladorFilter

class FlejesViewSet(viewsets.ModelViewSet):
    serializer_class = FlejesSimpleSerializer
    queryset = Flejes.objects.all()
    filterset_class = FlejesFilter

class FlejesListViewSet(viewsets.ModelViewSet):
    serializer_class = FlejesSerializer
    queryset = Flejes.objects.all()
    filterset_class = FlejesFilter

class FlejesProduccionDB(APIView):
    def get(self, request):
        return Response(leerFlejesProduccionDB())
    