from django.urls import path
from .views import (
    HomeView,
    AboutUsView,
    ServicesView,
    ContactUsView,
    DashboardView,
    Custom404View
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutUsView.as_view(), name='about_us'),
    path('services/', ServicesView.as_view(), name='services'),
    path('contact/', ContactUsView.as_view(), name='contact_us'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]

# Custom error handler
handler404 = Custom404View.as_view()
