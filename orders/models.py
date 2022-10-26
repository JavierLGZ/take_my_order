import datetime
from math import sqrt
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import requests


class Orders(models.Model):
    driver = models.IntegerField()
    pickup_lat = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    pickup_lng = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    delivery_lat = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    delivery_lng = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    delivery_init_time = models.DateTimeField()
    delivery_finish_time = models.DateTimeField()


    class Meta:
        ordering = ('delivery_init_time',)

    def __str__(self) -> str:
        return str(self.driver)

    def save(self, *args, **kwargs) -> None:
        self.driver = None
        min_length = 200
        stop_time = self.delivery_init_time + datetime.timedelta(minutes=59)
        active_orders_init = Orders.objects.filter(
            delivery_init_time__range = (self.delivery_init_time, stop_time)).values('driver')
        active_orders_finish = Orders.objects.filter(
            delivery_finish_time__range = (self.delivery_init_time, stop_time)).values('driver')
        
        print(active_orders_finish, active_orders_init)

        occupied_drivers = active_orders_init + active_orders_finish
        print(occupied_drivers)

        drivers_info = requests.get('https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json')
        drivers_info = drivers_info.json()
        for driver in drivers_info['alfreds']:
            print(driver['id'], occupied_drivers, type(driver['id']))
            if driver['id'] in occupied_drivers:
                print("no driver avalible")
                continue
            print("driver avalible")
            print(driver['lat'], driver['lng'], min_length)
            tot_lat = (self.pickup_lat - int(driver['lat']))**2
            tot_lng = (self.pickup_lng - int(driver['lng']))**2
            distance = sqrt(abs(tot_lat+tot_lng))
            if distance <= min_length:
                self.driver = driver['id']
                min_length = distance
                self.delivery_finish_time = stop_time
        super(Orders, self).save(*args, **kwargs)
