# models.py
from django.db import models

class ServiceType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.service_type.name}"


class Country(models.Model):
    code = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name
