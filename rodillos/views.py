from django.shortcuts import render
from rest_framework import viewsets
from rodillos.models import Seccion, Operacion, Posicion, Conjunto, Elemento, Rodillo, Montaje, Grupo, Material, Ficheros
from rodillos.serializers import ConjuntoSerializer, GruposSerializer
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination

class GrupoFilter(filters.FilterSet):
    class Meta:
        model = Grupo
        fields = {
            'nombre': ['exact'],
        }

class ConjuntoFilter(filters.FilterSet):
    class Meta:
        model = Conjunto
        fields = {
            'nombre': ['exact'],
        }

class ConjuntoViewSet(viewsets.ModelViewSet):
    serializer_class = ConjuntoSerializer
    queryset = Conjunto.objects.all()
    filterset_class = ConjuntoFilter
    
class GruposViewSet(viewsets.ModelViewSet):
    serializer_class = GruposSerializer
    queryset = Grupo.objects.all()
    filterset_class = GrupoFilter

