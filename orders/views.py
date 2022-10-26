from datetime import datetime, timedelta
from math import sqrt

import requests as rq
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Orders
from .serializers import OrderSerializer, OrderSerializerAll


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "driver",
                openapi.IN_QUERY,
                description=("ID del conductor para mostras pedidos activos"),
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description=("fecha de acceso a los pedidos en formato yyyy-mm-dd"),
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    ),
)
class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializerAll

    def get_queryset(self):
        driver_param = self.request.query_params.get("driver", None)
        date_param = self.request.query_params.get("date", None)
        print(type(driver_param), type(date_param))
        filter_data = self.get_serializer().Meta.model.objects
        if driver_param:
            filter_data = filter_data.filter(driver=int(driver_param))
        if date_param:
            filter_data = filter_data.filter(delivery_init_time__contains=date_param)
        return filter_data


class OrderDetail(generics.RetrieveDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer


class NewOrder(generics.CreateAPIView):
    # queryset = Orders.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        occupied_drivers = []
        order_data = request.data
        get_driver = None
        min_length = 200
        dit = datetime.strptime(order_data["delivery_init_time"], "%Y-%m-%dT%H:%M")
        stop_time = dit + timedelta(minutes=59)
        active_orders_init = Orders.objects.filter(
            delivery_init_time__range=(dit, stop_time)
        ).values()
        active_orders_finish = Orders.objects.filter(
            delivery_finish_time__range=(dit, stop_time)
        ).values()

        occupied_drivers = [driver["driver"] for driver in active_orders_init]
        occupied_drivers += [driver["driver"] for driver in active_orders_finish]

        drivers_info = rq.get(
            "https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json"
        )
        drivers_info = drivers_info.json()
        for driver in drivers_info["alfreds"]:
            if driver["id"] in occupied_drivers:
                continue
            tot_lat = (int(order_data["pickup_lat"]) - int(driver["lat"])) ** 2
            tot_lng = (int(order_data["pickup_lng"]) - int(driver["lng"])) ** 2
            distance = sqrt(abs(tot_lat + tot_lng))
            if distance <= min_length:
                get_driver = driver["id"]
                min_length = distance

        if not get_driver:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        delivery_finish_time = stop_time
        new_order = Orders.objects.create(
            driver=get_driver,
            pickup_lat=order_data["pickup_lat"],
            pickup_lng=order_data["pickup_lng"],
            delivery_lat=order_data["delivery_lat"],
            delivery_lng=order_data["delivery_lng"],
            delivery_init_time=order_data["delivery_init_time"],
            delivery_finish_time=delivery_finish_time,
        )
        new_order.save()

        serializer = OrderSerializer(new_order)
        return Response(serializer.data)
