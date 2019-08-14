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
        return f"{self.name}({self.dish} - {self.small_price})"


class Orders(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    topping = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="toppings")
    topping_steak = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="toppings_steak")
    #https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime - RuntimeWarning: DateTimeField received a naive datetime
    date = models.DateTimeField(default=timezone.now, blank=True)
    status = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.client} ordered {self.item} with {self.topping}/{self.topping_steak}"