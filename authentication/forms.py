from django import forms

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Enter your email", max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))