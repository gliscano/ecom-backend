
from carts.models import Cart
from rest_framework import serializers 
from stores.models import Store, Category, Product
from stores.serializers import ProductSerializer
 

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            'user_id',
            'product_id',
            'store_id',
            'date_created',
            'date_lastupdated',
            'status',
        )

        wrapper_name = 'cart'

        extra_kwargs = {
            'cart_id':{'write_only': True},
            'store_id':{'write_only': True},
            'user_id':{'write_only': True},
        }

class CartSerializerT(serializers.ModelSerializer):
    product_id = ProductSerializer(many=True, read_only = True)
    class Meta:
        model = Cart
        fields = (
            'user_id',
            'product_id',
            'store_id',
            'status',

        )
        
        extra_kwargs = {
            'product_id':{'read_only':True},
            'id':{'read_only':True},
        }