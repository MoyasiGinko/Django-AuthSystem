from django.views.generic import TemplateView, ListView, DetailView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import  ContactMessage
from django.contrib.auth.decorators import login_required






# HomePage View
class HomeView(TemplateView):
    template_name = 'realestate/home.html'

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

# Dashboard View
class DashboardView(LoginRequiredMixin, View):
    login_url = 'login'  # Redirects to this URL if the user is not logged in
    redirect_field_name = 'redirect_to'  # Field used for redirection

    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/dashboard.html", {"user": request.user})

# Custom 404 View
class Custom404View(TemplateView):
    template_name = 'realestate/404.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = 404
        return super().render_to_response(context, **response_kwargs)
