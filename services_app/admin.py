# admin.py
from django.contrib import admin
from .models import Service, ServiceType

admin.site.register(Service)
admin.site.register(ServiceType)
