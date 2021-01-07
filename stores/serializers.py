from rest_framework import serializers 
from stores.models import Store, Category, Product
 
 
class StoreSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Store
        fields = (
            'store_id',
            'name',
            'user_id',
            'description',
            'keywords',
            'logo_url',
            'banner_url',
            'title',
            'phone',
            'facebook',
            'instagram',
            'status',
        )

        wrapper_name = 'stores'


        extra_kwargs = {
            'user_id':{'write_only': True}
        }

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ( 'category_id','name', 'parent_category_id', 'subcategories')


class ProductSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Product
        fields = (
            'product_id',
            'code',
            'url_photos',
            'title',
            'description',
            'price',
            'stock',
            'status',
            'category_id',
            'store_id',
        )

        wrapper_name = 'products'


        extra_kwargs = {
            'category_id':{'write_only': True},
            'store_id':{'write_only': True}
        }
