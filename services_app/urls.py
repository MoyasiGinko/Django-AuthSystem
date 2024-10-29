# urls.py
from django.urls import path
from .views import service_list, service_create, service_type_create

urlpatterns = [
    path('list/', service_list, name='service_list'),
    path('create/', service_create, name='service_create'),
    path('create/service-type/', service_type_create, name='service_type_create'),
]
