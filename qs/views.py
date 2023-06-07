from rest_framework.views import APIView
from rest_framework.response import Response
from .qs import get_bd1

class EjesViewSet(APIView):
    def get(self, request):

        return Response(get_bd1())
    

