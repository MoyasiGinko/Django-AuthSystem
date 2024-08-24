from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .utils import account_activation_token


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry, this email is in use. Please choose another one.'}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry, this username is in use. Please choose another one.'}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'authentication/register.html', context)

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return render(request, 'authentication/register.html', context)

        if len(password) < 6:
            messages.error(request, 'Password is too short.')
            return render(request, 'authentication/register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()

        send_activation_email(request, user)
        messages.success(request, 'Account successfully created. Please check your email to activate your account.')
        if user.is_active is False:
            return redirect('activation_prompt', user_id=user.id)
        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if user.is_active:
                return redirect('login')

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, 'Account activated successfully')
                return redirect('login')
            else:
                messages.error(request, 'Activation link is invalid.')
                return redirect('activation_invalid')

        except DjangoUnicodeDecodeError:
            messages.error(request, 'Activation link is invalid.')
            return redirect('activation_invalid')

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f'Welcome, {user.username}. You are now logged in.')
                    return redirect('dashboard')
                messages.error(request, 'Account is not active. Please check your email.')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Please fill in all fields.')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('login')


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "dashboard/dashboard.html", {"user": request.user})


class ActivationSuccessView(View):
    def get(self, request):
        return render(request, 'authentication/activation_success.html')


class ActivationInvalidView(View):
    def get(self, request):
        return render(request, 'authentication/activation_invalid.html')


def activation_prompt(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    return render(request, "authentication/activation_prompt.html", {"user": user})


def send_activation_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    message = render_to_string('authentication/activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'activation_link': reverse('activate', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })
    })

    try:
        send_mail(
            mail_subject,
            message,
            None,
            [user.email],
            fail_silently=False,
        )
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    except Exception as e:
        return HttpResponse(f'Error: {e}')


def resend_activation_email(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user = get_object_or_404(get_user_model(), id=user_id)
        if not user.is_active:
            send_activation_email(request, user)
            messages.info(request, "Activation email sent. Please check your inbox.")
        else:
            messages.info(request, "Account is already activated.")
        return redirect('activation_prompt', user_id=user_id)
    return redirect('activation_prompt')


def activate_account_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = get_object_or_404(get_user_model(), email=email)
        if not user.is_active:
            send_activation_email(request, user)
            messages.info(request, "Activation email sent. Please check your inbox.")
        else:
            messages.info(request, "Account is already activated.")
        return redirect('login')
    return render(request, 'authentication/activate_account.html')
