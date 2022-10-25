from rest_framework import generics
from .models import Orders
from .serializers import OrderSerializer, OrderSerializerAll

class OrderList(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializerAll

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =Orders.objects.all()
    serializer_class = OrderSerializer