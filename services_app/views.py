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
