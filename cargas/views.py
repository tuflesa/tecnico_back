from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import AgenciaSerializer, CargaSerializer, CargaSimpleSerializer
from django_filters import rest_framework as filters
from .models import Agencia, Carga

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