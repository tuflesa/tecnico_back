from rest_framework.views import APIView
from rest_framework import viewsets
#from django.http import HttpResponse
from django_filters import rest_framework as filters
from rest_framework.response import Response
from .serializers import ArticuloSerializer
from .models import Articulo
from .qs import get_ejes, get_PC

#Filtros
class ArticuloFilter(filters.FilterSet):
    class Meta:
        model = Articulo
        fields = {
            'montajes': ['exact']
        }

# ViewSets
class EjesViewSet(APIView):
    def get(self, request):

        return Response(get_ejes())
    
class PCViewSet(APIView):
    def get(self, request):

        return Response(get_PC())
    
class ArticuloViewSet(viewsets.ModelViewSet):
    serializer_class = ArticuloSerializer
    queryset = Articulo.objects.all()
    filterset_class = ArticuloFilter

# def first(request):
#     return HttpResponse('1st message from views')