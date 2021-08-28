from carts.models import Cart
from carts.serializers import CartSerializer, CartSerializerT
from rest_framework import generics
from rest_framework import permissions


# Create your views here.


class CartList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Cart.objects.all()
    serializer_class = CartSerializerT

class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
