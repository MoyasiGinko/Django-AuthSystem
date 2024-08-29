from django.views.generic import TemplateView, ListView, DetailView, View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Property, ContactMessage

# HomePage View
class HomeView(TemplateView):
    template_name = 'realestate/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_properties'] = Property.objects.filter(is_featured=True)[:3]  # Example: Get 3 featured properties
        return context

# Property List View
class PropertyListView(ListView):
    model = Property
    template_name = 'realestate/property_list.html'
    context_object_name = 'properties'

# Property Detail View
class PropertyDetailView(DetailView):
    model = Property
    template_name = 'realestate/property_detail.html'
    context_object_name = 'property'

# About Us View
class AboutUsView(TemplateView):
    template_name = 'realestate/about_us.html'

# Services View
class ServicesView(TemplateView):
    template_name = 'realestate/services.html'

# Contact Us View
class ContactUsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'realestate/contact_us.html')

    def post(self, request, *args, **kwargs):

        # Process the form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save the message to the database
        ContactMessage.objects.create(name=name, email=email, message=message)

        # Redirect to the same page with a success message
        return render(request, 'realestate/contact_us.html', {'success': True})



# Profile View
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'realestate/profile.html'

# Dashboard View
class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'realestate/dashboard.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = Property.objects.filter(agent=self.request.user)
        return context

# Custom 404 View
class Custom404View(TemplateView):
    template_name = 'realestate/404.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = 404
        return super().render_to_response(context, **response_kwargs)
