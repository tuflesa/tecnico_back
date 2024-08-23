from rest_framework.views import APIView
from rest_framework.response import Response
from .qs import get_ejes, get_PC

class EjesViewSet(APIView):
    def get(self, request):

        return Response(get_ejes())
    
class PCViewSet(APIView):
    def get(self, request):

        return Response(get_PC())
