from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
import datetime

class Items(models.Model):
    name = models.CharField(max_length=64)
    dish = models.CharField(max_length=64)
    small_price = models.CharField(max_length=16)
    large_price = models.CharField(max_length=16, null=True)
    number_toppings = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f"{self.name}({self.dish})"


class Orders(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    topping = models.CharField(max_length=64, blank=True, default="none")
    topping_steak = models.CharField(max_length=64, blank=True, default="none")
    #https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime - RuntimeWarning: DateTimeField received a naive datetime
    price = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now, blank=True)
    status = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.client} ordered {self.item} with {self.topping}/{self.topping_steak}"

class Carts(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    ids = models.CharField(max_length=240)
    status = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.client} - {self.ids}"