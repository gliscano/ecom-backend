import json
from django.test import TestCase
from .models  import User, Address
#DRF
from rest_framework.test import APIClient
from rest_framework import status


# Create your tests here.

class UserTestCase(TestCase):

    def setUp(self):
        user = User(
            name = 'hugo',
            lastname = 'jimenez',
            username  = 'hjimenez',
            password = 'coldSnap3321',
        )

        user.save()

    def test_register_user(self):
        """ check if we can create user"""
        client = APIClient()
        response = client.post(
            '/api/v1/user/users/',{
                'name' :'ana',
                'lastname' :'victoria',
                'username' :'avictoria',
                'email':'avictoria@gmail.com',
                'password' :'coldSnap3321',
            },
             format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content),{"users":{"user_id":2,"name":"ana","lastname":"victoria","username":"avictoria","email":"avictoria@gmail.com","status":"inactive"}})