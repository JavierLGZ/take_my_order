from math import sqrt
import json
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import requests


class Orders(models.Model):
    driver = models.IntegerField()
    pickup_lat = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    pickup_lng = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    delivery_lat = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    delivery_lng = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    delivery_time = models.DateTimeField()

    class Meta:
        ordering = ('-delivery_time',)

    def __str__(self) -> str:
        return str(self.diver_id)

    def save(self, *args, **kwargs) -> None:
        self.driver = 0
        min_length = 200
        drivers_info = requests.get('https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json')
        drivers_info = drivers_info.json()
        for driver in drivers_info['alfreds']:
            tot_lat = (self.pickup_lat - int(driver['lat']))**2
            tot_lng = (self.pickup_lng - int(driver['lng']))**2
            tot = abs(tot_lat+tot_lng)
            distance = sqrt(tot)
            if distance <= min_length:
                self.driver = driver['id']
                min_length = distance
        super(Orders, self).save(*args, **kwargs)