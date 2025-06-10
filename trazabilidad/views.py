from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters import rest_framework as filters
from .serializers import AcumuladorSerializer, FlejesSerializer
from .models import Acumulador, Flejes
from .trazabilidad import leerFlejesProduccionDB

class AcumuladorFilter(filters.FilterSet):
    class Meta:
        model = Acumulador
        fields = {
            'zona__empresa__id': ['exact'],
        }

class AcumuladorViewSet(viewsets.ModelViewSet):
    serializer_class = AcumuladorSerializer
    queryset = Acumulador.objects.all()
    filterset_class = AcumuladorFilter

class FlejesViewSet(viewsets.ModelViewSet):
    serializer_class = FlejesSerializer
    queryset = Flejes.objects.all()


class FlejesProduccionDB(APIView):
    def get(self, request):
        return Response(leerFlejesProduccionDB())