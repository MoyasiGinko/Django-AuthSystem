# urls.py
from django.urls import path
from .views import service_list, service_create, service_type_create, country_city_view, load_cities, create_country, create_city

urlpatterns = [
    path('list/', service_list, name='service_list'),
    path('create/', service_create, name='service_create'),
    path('create/service-type/', service_type_create, name='service_type_create'),

    path('country-city/', country_city_view, name='country_city_view'),
    path('load-cities/', load_cities, name='load_cities'),  # AJAX URL for loading cities
    path('create-country/',create_country, name='create_country'),
    path('create-city/', create_city, name='create_city'),
]
