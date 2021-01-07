from rest_framework import serializers 
from users.models import User, Address
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import NotFound, ValidationError
from .utils import Util
from .models import CustomUser

from rest_framework import status
import json 

import secrets

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        return token

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
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
            }

    #def validate_password(self, value: str) -> str:

     
     #   return make_password(value)

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
            print(password)
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
            ValidationError('invalid Token', status=status.HTTP_400_BAD_REQUEST)
        validated_data['token'] = token

        return super(UserSerializer, self).create(validated_data)

class UserLoginSerilizer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)
        
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
        try:
            User.objects.get(user_id = validated_data['owner_id'])
        except:
            raise NotFound("User not found")
        return super(AddressSerializer, self).create(validated_data)


