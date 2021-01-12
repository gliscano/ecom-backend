import json
from users.models import User, Address, CustomUser
from users.serializers import UserSerializer, AddressSerializer, UserLoginSerilizer, MyTokenObtainPairSerializer, CustomUserSerializer
from rest_framework import generics
from rest_framework import permissions
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
import logging


logger = logging.getLogger(__name__)

class UserList(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()

        current_site = get_current_site(self.request).domain
        #relative_link = reverse('email_verify', kwargs={'token':instance.token,'pk':})

        absolute_url = 'http://example.domain.com/verify/email/'+ instance.token
        email_body = 'Hi ' + instance.name + ' use the link below to verify your email ' +absolute_url
        data = {
            'domain':absolute_url,
            'email_subject': 'Verify Your Email',
            'email_body': email_body,
            'email_reciver': instance.email,
        }
        Util.send_email(data)

class VerifyEmail(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny,)

    serializer_class = CustomUserSerializer
    http_method_names = ['patch']
    def patch(self, request, token):
        decoded_token = json.loads(Util.cryptograpy_text(token, False))
        try:
            user = CustomUser.objects.get(username=decoded_token['username'])
        except ObjectDoesNotExist:
            return Response('invalid token', status=status.HTTP_400_BAD_REQUEST)
        
        data = {'status':'active'}
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

class LoginUser(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)

    serializer_class = UserLoginSerilizer
    def post(self, request):
        try:
            user = User.objects.get(email=request.data['email'])
            if user['password'] != make_password(request.data['password']):
                return Response('Invalid crendentials', status=status.HTTP_401_UNAUTHORIZED)
            return Response({'token':'23232323232'})
        except ObjectDoesNotExist:
            return Response('Invalid token', status=status.HTTP_404_NOT_FOUND)
        
class ObtainTokenPairWithColorView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    serializer_class = MyTokenObtainPairSerializer


class CustomUserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    def get_serializer(self):
        return CustomUserSerializer

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                data = serializer.validated_data
                #current_site = get_current_site(self.request).domain
                #relative_link = reverse('email_verify', kwargs={'token':instance.token,'pk':})

                absolute_url = 'http://example.domain.com/verify/email/'+ user.token
                email_body = f'Hi {user.name} {user.lastname}, wellcome to the platform. Please use the link below to verify your email: {absolute_url}, enjoy the platform.'
                data = {
                    'email_subject': 'Account Activation',
                    'email_body': email_body,
                    'email_reciver': user.email,
                }
                Util.send_email(data)
            except Exception as e:
                if 'username' in str(e):
                    msg = 'username already taken' 
                elif 'email' in str(e):
                    msg = 'email already taken' 
                else:
                    msg = 'Internal Server Error' 
                logger.error(str(e))

                return Response({"msg":str(msg)}, status=status.HTTP_400_BAD_REQUEST)

            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class AddressList(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer




