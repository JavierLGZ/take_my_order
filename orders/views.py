from time import strptime
from rest_framework import generics
from .models import Orders
from .serializers import OrderSerializer, OrderSerializerAll
from datetime import datetime

class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializerAll
    def get_queryset(self):
        driver_param = self.request.query_params.get('driver', None)
        date_param = self.request.query_params.get('date', None)
        print(type(driver_param), type(date_param))
        filter_data = self.get_serializer().Meta.model.objects
        if driver_param:
            filter_data = filter_data.filter(driver = int(driver_param))
        if date_param:
            filter_data = filter_data.filter(delivery_time__contains = date_param)
        return filter_data


class OrderDetail(generics.RetrieveDestroyAPIView):
    queryset =Orders.objects.all()
    serializer_class = OrderSerializer

class NewOrder(generics.CreateAPIView):
    serializer_class = OrderSerializer
