from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Variante
from .serializers import VarianteSerializer

from .qs import get_ejes, get_PC, get_diametros_actuales_PLC, get_posiciones_actuales_PLC

# ViewSets
class EjesViewSet(APIView):
    def get(self, request):
        return Response(get_ejes())
    
class PCViewSet(APIView):
    def get(self, request):
        return Response(get_PC())
    
class DiametrosActPLC(APIView):
    def get(self, request):
        return Response(get_diametros_actuales_PLC())
    
class PosicionesActPLC(APIView):
    def get(self, request):
        return Response(get_posiciones_actuales_PLC())
    
class VarianteViewSet(viewsets.ModelViewSet):
    serializer_class = VarianteSerializer
    queryset = Variante.objects.all()