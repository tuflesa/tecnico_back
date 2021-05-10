from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import AplicacionSerializer, UserSerializer
from django.contrib.auth.models import User
from .models import Aplicacion

class AplicacionViewSet(viewsets.ModelViewSet):
    serializer_class = AplicacionSerializer
    queryset = Aplicacion.objects.all()

    def list(self, request):
        user = request.user
        queryset = self.get_queryset().filter(usuarios=user)
        serializer = AplicacionSerializer(queryset, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        usuario = UserSerializer(user, many=False)
        return Response({
            'token': token.key,
            'usuario': usuario.data
        })