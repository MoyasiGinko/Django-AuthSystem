from django import forms
from .models import Companyinfo, ContactMessage


class CompanyinfoForm(forms.ModelForm):
    class Meta:
        model = Companyinfo
        fields = [
            'company_name', 'logo', 'province_code', 'area_code',
            'address', 'phone1', 'phone2', 'company_email',
            'subscription_type', 'notes_and_description'
        ]


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}),
        }
