from django.shortcuts import render,redirect


# Create your views here.
from django.shortcuts import render,get_object_or_404
from App.serializers import *
from App.models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages


#REST FRAMEWORK
from rest_framework import status
from rest_framework.response import Response

#---------------------FUNCTION VIEW-------------------------
from rest_framework.decorators import api_view

#------------------------CLASS BASED VIEW-------------------
from rest_framework.views import APIView


#------------------------GENERIC VIEWs-------------------
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


#------------------------ VIEW SETS-------------------
from rest_framework.viewsets import ModelViewSet


#------FILTERS, SEARCH AND ORDERING
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter,OrderingFilter

#------PAGINATION-------------
from rest_framework.pagination import PageNumberPagination




#----------------CREATING A CART------------------------
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from App.serializers import *
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics,status
from rest_framework.decorators import api_view

# Create your views here.

# class UserView(APIView):

#   def get(self,request, format=None):
#       return Response("User Account View", status=200)

#   def post(self,request, format=None):

#       return Response("Creating User", status=200)



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# class RegistrationView(generics.CreateAPIView):
#     queryset = MyUser.objects.all()
#     serializer_class = DjangoReactUserSerializer
#     permission_classes = (permissions.AllowAny,)

# class ReactLoginView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = DjangoReactUserSerializer
    
#     def create(self, request, *args, **kwargs):
#         user = self.get_object()
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authtoken.models import Token




















#----------------HIZI NI KWA AJILI YA APIS ------------------------------
class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            username = serializer.validated_data.get('username')
            phone = serializer.validated_data.get('phone')
            # last_name = serializer.validated_data.get('last_name')
            
            if MyUser.objects.filter(email=email).exists():
                return Response({'error': 'email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            if MyUser.objects.filter(username=username).exists():
                return Response({'error': 'username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            

            user = MyUser.objects.create_user(email=email, password=password, username=username, phone=phone)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReactLoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)





class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            Token.objects.filter(user=user).delete()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)





class UserDataView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # Assuming you have a serializer for User data
        serializer = UserDataSerializer(user)
        return Response(serializer.data)

