from django.shortcuts import render
from .serializers import ArticuloSerializer
from .models import Articulo

#Filtros
class ArticuloFilter(filters.FilterSet):
    class Meta:
        model = Articulo
        fields = {
            'montajes': ['exact']
        }

class ArticuloViewSet(viewsets.ModelViewSet):
    serializer_class = ArticuloSerializer
    queryset = Articulo.objects.all()
    filterset_class = ArticuloFilter
