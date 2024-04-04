from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import AgenciaSerializer, CargaSerializer, CargaSimpleSerializer, BasculaSerializer, LlamadaSimpleSerializer, UltimasLlamadasSerializer
from django_filters import rest_framework as filters
from .models import Agencia, Carga, Bascula, Llamada

class AgenciaFilter(filters.FilterSet):
    class Meta:
        model = Agencia
        fields = {
            'nombre': ['icontains'],
            'observaciones': ['icontains']
        }

class AgenciaViewSet(viewsets.ModelViewSet):
    serializer_class = AgenciaSerializer
    queryset = Agencia.objects.all()
    filterset_class = AgenciaFilter

class BasculaViewSet(viewsets.ModelViewSet):
    serializer_class = BasculaSerializer
    queryset = Bascula.objects.all()

class CargaFilter(filters.FilterSet):
    class Meta:
        model = Carga
        fields = {
            'empresa': ['exact'],
            'fecha_entrada': ['exact'],
            'bruto': ['isnull']
        }

class CargaListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CargaSerializer
    queryset = Carga.objects.all().order_by('fecha_entrada', 'hora_entrada')
    filterset_class = CargaFilter

class CargaViewSet(viewsets.ModelViewSet):
    serializer_class = CargaSimpleSerializer
    queryset = Carga.objects.all()
    filterset_class = CargaFilter

class LlamadaViewSet(viewsets.ModelViewSet):
    serializer_class = LlamadaSimpleSerializer
    queryset = Llamada.objects.all()

class UltimasLlamadasFilter(filters.FilterSet):
    class Meta:
        model = Llamada
        fields = {
            'carga__empresa': ['exact'],
            'carga__bruto': ['isnull']
        }

class UltimasLlamadasViewSet(viewsets.ModelViewSet):
    serializer_class = UltimasLlamadasSerializer
    queryset = Llamada.objects.all().order_by('-fecha', '-hora')
    filterset_class = UltimasLlamadasFilter