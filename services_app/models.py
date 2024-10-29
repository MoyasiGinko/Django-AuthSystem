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
