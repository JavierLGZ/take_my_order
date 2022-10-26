from dataclasses import fields

from rest_framework import serializers

from .models import Orders


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = (
            "pickup_lat",
            "pickup_lng",
            "delivery_lat",
            "delivery_lng",
            "delivery_init_time",
        )


class OrderSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = (
            "id",
            "driver",
            "pickup_lat",
            "pickup_lng",
            "delivery_lat",
            "delivery_lng",
            "delivery_init_time",
        )
