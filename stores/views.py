from stores.models import Product, Category, Store
from stores.serializers import ProductSerializer, CategorySerializer, StoreSerializer
from rest_framework import generics

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.filter(parent_category_id=None)
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.filter(parent_category_id=None)
    serializer_class = CategorySerializer

class SubCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    
class StoreList(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class StoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer