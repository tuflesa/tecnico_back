from django.db.models import fields
from django.shortcuts import render
from rest_framework import viewsets

from repuestos.models import Contacto
from .serializers import DireccionesEmpresaSerializer, EmpresaSerializer, ZonaSerializer, SeccionSerializer, EquipoSerializer
from .models import Direcciones, Empresa, Zona, Seccion, Equipo
from django_filters import filterset, rest_framework as filters

class ZonasFilter(filters.FilterSet):
    class Meta:
        model = Zona
        fields = {
            'empresa': ['exact'],
            'nombre': ['icontains'],
            'siglas': ['icontains']
        }

class DireccionesFilter(filters.FilterSet):
    class Meta:
        model = Direcciones
        fields = {
            'empresa': ['exact']
        }

class SeccionFilter(filters.FilterSet):
    class Meta:
        model = Seccion
        fields = {
            'zona__empresa': ['exact'],
            'zona': ['exact'],
            'nombre': ['icontains']
        }

class EquipoFilter(filters.FilterSet):
    class Meta:
        model = Equipo
        fields = {
            'seccion': ['exact'],
            'seccion__zona': ['exact'],
            'seccion__zona__empresa': ['exact'],
            'nombre': ['icontains'],
            'fabricante': ['icontains'],
            'modelo': ['icontains'],
            'numero': ['icontains']
        }

class EmpresaViewSet(viewsets.ModelViewSet):
    serializer_class = EmpresaSerializer
    queryset = Empresa.objects.all()

class DireccionesEmpresaViewSet(viewsets.ModelViewSet):
    serializer_class = DireccionesEmpresaSerializer
    queryset = Direcciones.objects.all()
    filterset_class = DireccionesFilter

class ZonaViewSet(viewsets.ModelViewSet):
    serializer_class = ZonaSerializer
    queryset = Zona.objects.all()
    filterset_class = ZonasFilter

class SeccionViewSet(viewsets.ModelViewSet):
    serializer_class = SeccionSerializer
    queryset = Seccion.objects.all()
    filterset_class = SeccionFilter

class EquipoViewSet(viewsets.ModelViewSet):
    serializer_class = EquipoSerializer
    queryset = Equipo.objects.all()
    filterset_class = EquipoFilter