from django.db import models
from users.models import User, CustomUser

# Create your models here.

class Store(models.Model):
    STATUS_CHOICES = (
        ('active','Active'),
        ('inactive','Inactive'),
        ('suspended','Suspended'),
        ('deleted','deleted'),
    )
    store_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 100, blank = False)
    description = models.CharField(max_length = 200, blank = False)
    keywords = models.CharField(max_length = 200, blank = False)
    logo_url = models.CharField(max_length = 200, blank = False)
    banner_url = models.CharField(max_length = 200, blank = False)
    title = models.CharField(max_length = 100, blank = False)
    phone = models.CharField(max_length = 100, blank = False)
    facebook = models.CharField(max_length = 200, blank = False)
    instagram = models.CharField(max_length = 200, blank = False)
    status = models.CharField(max_length = 20, choices=STATUS_CHOICES,default='active')
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'owner_id')
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, blank = False )
    date_lastupdated = models.DateTimeField(auto_now=True, auto_now_add=False,blank = False)

class Category(models.Model):
    category_id = models.AutoField(primary_key = True)     
    parent_category_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategories')
    name = models.CharField(max_length = 100, blank = False)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, blank = False )
    date_lastupdated = models.DateTimeField(auto_now=True, auto_now_add=False,blank = False)  

class Product(models.Model):
    STATUS_CHOICES = (
        ('active','Active'),
        ('inactive','Inactive'),
        ('suspended','Suspended'),
        ('deleted','deleted'),
    )
    product_id = models.AutoField(primary_key = True)
    code = models.CharField(max_length = 100, blank = False)
    url_photos = models.CharField(max_length = 200, blank = False)
    title = models.CharField(max_length = 200, blank = False)
    description = models.CharField(max_length = 200, blank = False)
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    status = models.CharField(max_length = 20,  choices=STATUS_CHOICES,default='active')
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, blank = False )
    date_lastupdated = models.DateTimeField(auto_now=True, auto_now_add=False,blank = False)
    category_id = models.ManyToManyField(Category)    
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)    

    class Meta:
        ordering = ('date_created',)