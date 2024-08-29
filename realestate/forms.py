from django import forms
from .models import Property, ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

    # Optional: You can customize widgets for better control over rendering
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
        'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}),
    }


# Property Form (if you need one for agents to add/edit properties)
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'location', 'bedrooms', 'bathrooms', 'area', 'property_type', 'image', 'is_featured']
