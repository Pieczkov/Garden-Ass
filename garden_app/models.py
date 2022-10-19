from datetime import date

from django.contrib.auth.models import User
from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"


class PlantType(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return f"Plant type -- {self.name}"


class Plant(models.Model):
    name = models.CharField(max_length=60)
    species = models.CharField(null=True, blank=True, max_length=60)
    description = models.TextField(blank=True, null=True)
    amount = models.IntegerField(default=1)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    type = models.ForeignKey(PlantType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.type.name}"


class PlanOfWork(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    created = models.DateField(auto_now=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    plant = models.ForeignKey(Plant, default=None, null=True, blank=True, on_delete=models.CASCADE)
    plan = models.ManyToManyField(PlanOfWork, blank=True)

    def __str__(self):
        return f"{self.name}"


# class CoWorker(models.Model):
#     first_name = models.CharField(max_length=60)
#     last_name = models.CharField(max_length=60)
#     plant = models.ManyToManyField(Plants)
#     work_to_do = models.ManyToManyField(WorkToDo)
#     plan = models.ManyToManyField(PlanOfWork)
#     gardener = models.ForeignKey(User)
