from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer
class RegisterView(generics.CreateAPIView): serializer_class=RegisterSerializer; permission_classes=[AllowAny]
class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        user=authenticate(request, username=request.data.get('username',''), password=request.data.get('password',''))
        if not user: return Response({'detail':'Invalid username or password.'},status=400)
        login(request,user); return Response({'user':UserSerializer(user).data,'csrfToken':get_token(request)})
class LogoutView(APIView):
    def post(self,request): logout(request); return Response(status=status.HTTP_204_NO_CONTENT)
class MeView(APIView):
    def get(self,request): return Response({'user':UserSerializer(request.user).data,'csrfToken':get_token(request)})
