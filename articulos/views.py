from django.shortcuts import render
from .serializers import ArticuloSerializer, FormasSerializer, CalidadSerializer, AcabadoSerializer, NormaSerializer
from django_filters import rest_framework as filters
from rest_framework import viewsets
from .models import Articulo, Formas, Calidad, Acabado, Norma

#Filtros
class ArticuloFilter(filters.FilterSet):
    class Meta:
        model = Articulo
        fields = {
            'montajes': ['exact'],
            'nombre': ['exact'],
        }

class ArticuloViewSet(viewsets.ModelViewSet):
    serializer_class = ArticuloSerializer
    queryset = Articulo.objects.all()
    filterset_class = ArticuloFilter

class FormasViewSet(viewsets.ModelViewSet):
    serializer_class = FormasSerializer
    queryset = Formas.objects.all()
 
 
class CalidadViewSet(viewsets.ModelViewSet):
    serializer_class = CalidadSerializer
    queryset = Calidad.objects.all()
 
 
class AcabadoViewSet(viewsets.ModelViewSet):
    serializer_class = AcabadoSerializer
    queryset = Acabado.objects.all()
 
 
class NormaViewSet(viewsets.ModelViewSet):
    serializer_class = NormaSerializer
    queryset = Norma.objects.all()
