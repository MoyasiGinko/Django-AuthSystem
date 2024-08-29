from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Agent Model
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# Property Model
class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area = models.IntegerField(help_text="Size in square feet")
    property_type = models.CharField(max_length=50, choices=[('house', 'House'), ('apartment', 'Apartment')])
    image = models.ImageField(upload_to='property_images/')
    listed_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-listed_date']

# ContactMessage Model
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

# Additional Models
# You can add more models as needed, such as 'Appointment', 'PropertyInquiry', etc.
