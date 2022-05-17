from importlib.metadata import distribution
from operator import truediv
from django.db import models
import re
from datetime import date

# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self) -> list:
        
        distribution = []
        fill:float = self.passengers / 2
        integer_part = round(fill)
        decimal_part = fill - round(fill)

        for i in range(integer_part):
            distribution.append([True,True])

        if decimal_part != 0:
            distribution.append([True,False])

class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def is_finished(self) -> bool:
        if self.end == date.today():
            return True
        return False


def test_valid_number_plate(number_plate:str) -> bool:
    regx = "^[A-Z]{2}-\d{2}-\d{2}$"
    if re.match(regx, number_plate):
        return True
    return False