import requests
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework import status
from rest_framework.response import Response


class Orders(models.Model):
    driver = models.IntegerField()
    pickup_lat = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    pickup_lng = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    delivery_lat = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    delivery_lng = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    delivery_init_time = models.DateTimeField()
    delivery_finish_time = models.DateTimeField()

    class Meta:
        ordering = ("delivery_init_time",)

    def __str__(self) -> str:
        return str(self.driver)
