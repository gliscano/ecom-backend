import json
from users import serializers
from users.models import User, Address, CustomUser
from stores.models import Store
from stores.serializers import StoreSerializer
from users.serializers import UserSerializer, AddressSerializer, UserLoginSerilizer, MyTokenObtainPairSerializer, CustomUserSerializer, ForgotPasswordSerilizer, ResetPasswordSerilizer, MyTokenRefreshPairSerializer
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

class UserList(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


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
        serializer = CustomUserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

class ResetPassword(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny,)

    serializer_class = CustomUserSerializer
    http_method_names = ['post']
    def post(self, request, token):
        try:
            decoded_token = json.loads(Util.cryptograpy_text(token, False))
            user = CustomUser.objects.get(username=decoded_token['username'])
        except ObjectDoesNotExist:
            return Response('invalid token', status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response('invalid token', status=status.HTTP_400_BAD_REQUEST)
            
        data = {'password':make_password(request.data['password'])}
        print(request.data['password'])
        serializer = CustomUserSerializer(user ,data=data,  partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({})

class ChangePassword(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ForgotPasswordSerilizer
    http_method_names = ['post']

    def post(self, request):
        serializer = ForgotPasswordSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = CustomUser.objects.get(email=request.data['email'])
        except ObjectDoesNotExist:
            return Response('invalid email', status=status.HTTP_400_BAD_REQUEST)
        token = Util.cryptograpy_text(json.dumps({
            'email': user.email,
            'username': user.username,
        }))

        absolute_url = 'http://example.domain.com/reset_password/'+ token
        email_body = f"Hi Please use the link below to change your password your email: {absolute_url}, If you didn't request the password change please ignore this email. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum" 
        data = {
            'email_subject': 'Change password security system',
            'email_body': email_body,
            'email_reciver': user.email,
        }
        Util.send_email(data)
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
        
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class MyTokenRefreshPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenRefreshPairSerializer


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
                email_body = f'Hi {user.name} {user.lastname}, wellcome to the platform. Please use the link below to verify your email: {absolute_url}, enjoy the platform.  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'
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


class ResendEmailInfo(APIView):
    def post(self, request, format='json'):
        return Response(json, status=status.HTTP_201_CREATED)


class UserInfoAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user

class UserAddressInfoAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddressSerializer

    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(owner_id=user.id, owner_type='user')


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class AddressList(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)

    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    #add handler for store
    def get_object(self):
        user = self.request.user
        return Address.objects.filter(address_id=id,owner_id=user.id, owner_type='user')




class UserStorelist(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.filter(user_id=self.kwargs['pk'])
