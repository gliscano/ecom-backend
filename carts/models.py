from django.db import models

# Create your models here.
from django.db import models
from users.models import User, CustomUser
from stores.models import Store, Product


# Create your models here.


class Cart(models.Model):
    STATUS_CHOICES = (
        ('active','Active'),
        ('inactive','Inactive'),
        ('suspended','Suspended'),
        ('deleted','deleted'),
    )
    cart_id = models.AutoField(primary_key = True)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, related_name = 'store_cart_id')
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'user_cart_id')
    product_id = models.ManyToManyField(Product)    
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, blank = False )
    date_lastupdated = models.DateTimeField(auto_now=True, auto_now_add=False,blank = False)
    status = models.CharField(max_length = 20, choices=STATUS_CHOICES,default='active')

