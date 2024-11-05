# views.py
from django.shortcuts import render, redirect
from .models import Service, ServiceType

def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {'services': services})

def service_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        service_type_id = request.POST.get('service_type')
        description = request.POST.get('description')

        # Get the service type object by ID
        service_type = ServiceType.objects.get(id=service_type_id)

        # Create and save the new service
        Service.objects.create(name=name, service_type=service_type, description=description)

        return redirect('service_list')

    # Fetch all service types to populate the dropdown
    service_types = ServiceType.objects.all()
    return render(request, 'services/service_form.html', {'service_types': service_types})

def service_type_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        ServiceType.objects.create(name=name)
        return redirect('service_list')

    return render(request, 'services/service_type_form.html')



# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Country, City

def country_city_view(request):
    countries = Country.objects.all()
    cities = []
    selected_country_id = request.GET.get('country')

    if selected_country_id:
        # Fetch cities only if a country is selected
        cities = City.objects.filter(country_id=selected_country_id)

    context = {
        'countries': countries,
        'cities': cities,
        'selected_country_id': selected_country_id,
    }
    return render(request, 'services/country_city.html', context)

def load_cities(request):
    country_id = request.GET.get('country_id')
    if not country_id:
        return JsonResponse({"error": "Country ID not provided"}, status=400)

    # Fetch only the cities belonging to the selected country
    cities = City.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)



from django.shortcuts import render, redirect
from .models import Country, City

def create_country(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        name = request.POST.get('name')
        if code and name:  # Basic validation
            Country.objects.create(code=code, name=name)
            return redirect('country_city_view')  # Replace 'country_list' with the actual URL for listing countries
    return render(request, 'services/create_country.html')

def create_city(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        name = request.POST.get('name')
        country_id = request.POST.get('country')
        try:
            country = Country.objects.get(id=country_id)
            if code and name and country:  # Basic validation
                City.objects.create(code=code, name=name, country=country)
                return redirect('country_city_view')  # Replace 'city_list' with the actual URL for listing cities
        except Country.DoesNotExist:
            # Handle the case where the country ID is invalid
            pass
    countries = Country.objects.all()  # For dropdown selection
    return render(request, 'services/create_city.html', {'countries': countries})
