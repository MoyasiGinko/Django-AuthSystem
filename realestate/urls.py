from django.urls import path
from .views import (
    HomeView,
    AboutUsView,
    ServicesView,
    ContactUsView,
    DashboardView,
    Custom404View,
    create_companyinfo,
    edit_companyinfo
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutUsView.as_view(), name='about_us'),
    path('services/', ServicesView.as_view(), name='services'),
    path('contact/', ContactUsView.as_view(), name='contact_us'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('create-company/', create_companyinfo, name='create_companyinfo'),
    path('edit_companyinfo/<int:pk>/', edit_companyinfo, name='edit_companyinfo'),
]

# Custom error handler
handler404 = Custom404View.as_view()
