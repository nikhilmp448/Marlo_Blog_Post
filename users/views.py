from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from .models import Account
from django.core.cache import BaseCache
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# register
class UserRegisterViewset(viewsets.ViewSet):

    def create(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
## logout user   
class UserLogoutView(APIView):
    def post(self, request):
        token = request.auth  # Access token from the request
        if token:
            # Store the token in the cache with a specific timeout (blacklist the token)
            BaseCache.add(f'blacklisted_token_{token}', None, timeout=token.lifetime.total_seconds())
            return Response({"message": "Token has been blacklisted"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)
        
## login user    
class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

## update retrieve delete my account
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user