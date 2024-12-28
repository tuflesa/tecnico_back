from rest_framework.views import APIView
#from rest_framework import viewsets
#from django.http import HttpResponse
from django_filters import rest_framework as filters
from rest_framework.response import Response

from .qs import get_ejes, get_PC

# ViewSets
class EjesViewSet(APIView):
    def get(self, request):

        return Response(get_ejes())
    
class PCViewSet(APIView):
    def get(self, request):

        return Response(get_PC())

# def first(request):
#     return HttpResponse('1st message from views')