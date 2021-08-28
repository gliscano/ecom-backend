from rest_framework import serializers 
from users.models import User, Address, CustomUser
from stores.models import Store
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import NotFound, ValidationError, ParseError
from .utils import Util

from rest_framework.response import Response

from rest_framework import status
import json 

import secrets
import traceback

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
            data = super().validate(attrs)
            refresh = self.get_token(self.user)
            # Add extra responses here
            data.update({'user_id':self.user.id})
            return data
            
class MyTokenRefreshPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
            data = super().validate(attrs)
            return data

    
class CustomUserSerializer(serializers.ModelSerializer):
    label = None
    allow_null = None
    #user_id = serializers.CharField(source='id')

    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ( 
            'username', 
            'password',
            'name',
            'lastname',
            'username',
            'email',
            'status')
        extra_kwargs = {
            'password': {'write_only': True},
            'token  ': {'write_only': True},
            'status  ': {'read_only': True},
            'id  ': {'read_only': True},
            }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        try:
            token = Util.cryptograpy_text(json.dumps({
                'email': validated_data['email'],
                'username': validated_data['username'],
            }))
        except:
            ValidationError('invalid Token', status=status.HTTP_400_BAD_REQUEST)
        validated_data['token'] = token
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
 
class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = (
            'user_id',
            'name',
            'lastname',
            'username',
            'email',
            'status'
        )
        wrapper_name = 'users'
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'token  ': {'write_only': True},
            'status  ': {'read_only': True},
            }

        

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        try:
            token = Util.cryptograpy_text(json.dumps({
                'email': validated_data['email'],
                'username': validated_data['username'],
            }))
        except:
            return Response('invalid Token', status=status.HTTP_400_BAD_REQUEST)
        validated_data['token'] = token

        return super(UserSerializer, self).create(validated_data)
def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')

class UserLoginSerilizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'password',
        )
        extra_kwargs = {
        'email  ': {'required': True},
        }

  
class ForgotPasswordSerilizer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = (
            'email',
        )
        extra_kwargs = {
        'email  ': {'read_only': True},
        }

  
  
class ResetPasswordSerilizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'password',
        )
        extra_kwargs = {
            'password  ': {'required': True,'write_only':True},
        }

  

class AddressSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Address
        fields = (
            'address_id',
            'owner_id',
            'owner_type',
            'property_type',
            'property_id',
            'city',
            'state',
            'street',
            'postal_code',
            'extra_info',
        )

        wrapper_name = 'address'


    def create(self, validated_data):
        if validated_data['owner_type'] != 'user' and validated_data['owner_type'] != 'store':
            raise serializers.ValidationError('invalid owner_type')
       
        try:
            if validated_data['owner_type'] == 'user':
                CustomUser.objects.get(id = 8)
            elif validated_data['owner_type'] == 'store':
                Store.objects.get(store_id = validated_data['owner_id'])
            
        except Exception as e:
            raise NotFound("Owner not found")
        return super(AddressSerializer, self).create(validated_data)


