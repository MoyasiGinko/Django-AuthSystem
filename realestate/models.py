from django.db import models
from django.contrib.auth.models import User


class Companyinfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_info')
    company_name = models.CharField(max_length=30)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    province_code = models.CharField(max_length=2)
    area_code = models.CharField(max_length=4)
    address = models.CharField(max_length=100)
    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, null=True, blank=True)
    company_email = models.EmailField()
    registration_date = models.DateField(auto_now_add=True)
    current_activation_date = models.DateField(null=True, blank=True)
    expiry_current_activation = models.DateField(null=True, blank=True)
    subscription_type = models.CharField(max_length=1, choices=[('1', 'Free'), ('2', 'Paid')])
    member_activation_status = models.CharField(max_length=1, choices=[('A', 'Active'), ('I', 'Inactive')])
    notes_and_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.company_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
