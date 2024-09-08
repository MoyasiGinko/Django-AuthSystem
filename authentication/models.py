from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator

class CustomUser(AbstractUser):
    username = models.CharField(max_length=10, unique=True)  # Ensure username is unique
    password = models.CharField(max_length=128, validators=[MinLengthValidator(8)])  # Corrected password field
    company_name = models.CharField(max_length=30, blank=True, null=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    province_code = models.CharField(max_length=2, blank=True, null=True)
    area_code = models.CharField(max_length=4, blank=True, null=True)
    address = models.CharField(max_length=30, blank=True, null=True)
    phone1 = models.CharField(max_length=15, blank=True, null=True)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    registration_date = models.DateField(auto_now_add=True)
    current_activation_date = models.DateField(blank=True, null=True)
    expiry_current_activation = models.DateField(blank=True, null=True)
    subscription_type = models.CharField(max_length=1, choices=[('F', 'Free'), ('P', 'Paid')], default='F')
    mem_activation_status = models.CharField(max_length=1, choices=[('A', 'Active'), ('I', 'Inactive')], default='I')
    note_and_description = models.TextField(blank=True, null=True)
