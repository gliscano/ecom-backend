from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(models.Model):
    STATUS_CHOICES = (
        ('active','Active'),
        ('inactive','Inactive'),
        ('suspended','Suspended'),
        ('deleted','deleted'),
    )

    user_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 70, blank = False)
    password = models.CharField(max_length = 255, blank = False)
    token = models.CharField(max_length = 255, blank = True)
    lastname = models.CharField(max_length = 70, blank = False)
    username = models.CharField(max_length = 70, blank = False, unique=True)
    email = models.EmailField(max_length = 254, blank = False, unique=True)
    status = models.CharField(max_length = 20, choices=STATUS_CHOICES,default='inactive')
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, blank = False )
    date_lastupdated = models.DateTimeField(auto_now=True, auto_now_add=False,blank = False)

class CustomUser(AbstractUser):
    STATUS_CHOICES = (
        ('active','Active'),
        ('inactive','Inactive'),
        ('suspended','Suspended'),
        ('deleted','deleted'),
    )
    name = models.CharField(max_length = 70, blank = False)
    lastname = models.CharField(max_length = 70, blank = False)
    token = models.CharField(max_length = 255, blank = True)
    email = models.EmailField(max_length = 254, blank = False, unique=True)
    username = models.CharField(max_length = 70, blank = False, unique=True)
    status = models.CharField(max_length = 20, choices=STATUS_CHOICES,default='inactive')
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, blank = False )
    date_lastupdated = models.DateTimeField(auto_now=True, auto_now_add=False,blank = False)




class Address(models.Model):
    TYPE_OWNER = (
        ('user','User'),
        ('store','Store'),
    )
    address_id = models.AutoField(primary_key = True)
    owner_id = models.CharField(max_length = 50, blank = False)
    owner_type = models.CharField(max_length = 30,choices=TYPE_OWNER, blank = False)
    property_type = models.CharField(max_length = 50, blank = False)
    property_id = models.CharField(max_length = 20, blank = False)
    city = models.CharField(max_length = 100, blank = False)
    state = models.CharField(max_length = 100, blank = False)
    street = models.CharField(max_length = 100, blank = False)
    postal_code = models.CharField(max_length = 20, blank = False)
    extra_info = models.CharField(max_length = 200, blank = True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, blank = False )
    date_lastupdated = models.DateTimeField(auto_now=True, auto_now_add=False,blank = False)

    