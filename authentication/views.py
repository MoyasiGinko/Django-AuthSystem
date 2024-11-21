from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import json
from django.http import JsonResponse, HttpResponse
from .models import CustomUser
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
from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth.tokens import default_token_generator
from .forms import PasswordResetRequestForm
from django.views.generic import TemplateView




User = get_user_model()

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
        company_name = request.POST.get('companyname')
        province_code = request.POST.get('provincecode')
        area_code = request.POST.get('areacode')
        address = request.POST.get('address')
        phone1 = request.POST.get('phone1')
        phone2 = request.POST.get('phone2', '')
        note_and_description = request.POST.get('noteandescription', '')
        company_logo = request.FILES.get('company_logo')

        context = {
            'fieldValues': request.POST
        }

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'authentication/register.html', context)

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return render(request, 'authentication/register.html', context)

        if len(password) < 6:
            messages.error(request, 'Password is too short.')
            return render(request, 'authentication/register.html', context)

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            company_name=company_name,
            province_code=province_code,
            area_code=area_code,
            address=address,
            phone1=phone1,
            phone2=phone2,
            note_and_description=note_and_description
        )

        user.company_logo = company_logo
        user.set_password(password)
        user.is_active = False
        user.save()

        # Send activation email and show success message
        send_activation_email(request, user)
        messages.success(request, 'Account successfully created. Please check your email to activate your account.')

        return redirect('activation_prompt', user_id=user.id)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            # if user.is_active:
            #     return redirect('login')

            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, 'Account activated successfully')
                return redirect('activation_success')
            else:
                messages.error(request, 'Activation link is invalid.')
                return redirect('activation_invalid')

        except DjangoUnicodeDecodeError:
            messages.error(request, 'Activation link is invalid.')
            return redirect('activation_invalid')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            # Authenticate user based on provided username and password
            user = auth.authenticate(username=username, password=password)

            if user:
                # Check if the user is active
                if user.is_active:
                    # Check membership activation status
                    if user.mem_activation_status == 'A':  # Assuming 'A' means 'Active'
                        auth.login(request, user)
                        messages.success(request, f'Welcome, {user.username}. You are now logged in.')
                        return redirect('profile')
                    else:
                        # If membership is inactive, show a message to renew membership
                        messages.error(request, 'Your membership is inactive. Please renew your membership.')
                        return render(request, 'authentication/login.html')

                # Account is not active
                messages.error(request, 'Account is not active. Please check your email.')
                return render(request, 'authentication/login.html')

            # Invalid credentials
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'authentication/login.html')

        # Fields are not filled in
        messages.error(request, 'Please fill in all fields.')
        return render(request, 'authentication/login.html')



class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('login')



class ProfileView(LoginRequiredMixin, View):
    template_name = 'authentication/profile.html'
    login_url = 'login'  # Redirects to this URL if the user is not logged in
    redirect_field_name = 'redirect_to'  # Field used for redirection

    def get(self, request, *args, **kwargs):
        # Passing the logged-in user's data to the template
        return render(request, self.template_name, {"user": request.user})



class ActivationSuccessView(View):
    def get(self, request):
        return render(request, 'authentication/activation_success.html')


class ActivationInvalidView(View):
    def get(self, request):
        return render(request, 'authentication/activation_invalid.html')


class ActivationPromptView(View):
    def get(self, request, user_id):
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


class ResendActivationEmailView(View):
    def post(self, request):
        user_id = request.POST.get('user_id')
        user = get_object_or_404(get_user_model(), id=user_id)
        if not user.is_active:
            send_activation_email(request, user)
            messages.info(request, "Activation email sent. Please check your inbox.")
        else:
            messages.info(request, "Account is already activated.")
        return redirect('activation_prompt', user_id=user_id)

    def get(self, request):
        return redirect('activation_prompt')



class ActivateAccountView(View):
    def get(self, request):
        return render(request, 'authentication/activate_account.html')

    def post(self, request):
        email = request.POST.get('email')
        if not email:
            messages.error(request, "Email field cannot be empty.")
            return render(request, 'authentication/activate_account.html')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with this email address.")
            return render(request, 'authentication/activate_account.html')

        if not user.is_active:
            send_activation_email(request, user)
            messages.info(request, "Activation email sent. Please check your inbox.")
        else:
            messages.info(request, "Account is already activated.")

        return redirect('login')



class PasswordResetRequestView(View):
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, 'authentication/password_reset_request.html', {'form': form})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                current_site = get_current_site(request)
                mail_subject = 'Reset your password'
                message = render_to_string('authentication/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'reset_token': reverse('password_reset_confirm', kwargs={
                        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user)
        })
                })
                send_mail(mail_subject, message, None, [email])
                messages.success(request, 'We have sent you an email to reset your password.')
            else:
                messages.error(request, 'No user is associated with this email address.')
            return redirect('password_reset_request')
        return render(request, 'authentication/password_reset_request.html', {'form': form})


class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return render(request, 'authentication/password_reset_confirm.html', {'validlink': True, 'user': user})
        else:
            messages.error(request, 'The password reset link was invalid, possibly because it has already been used.')
            return redirect('password_reset_request')

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')

            if password != password_confirm:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'authentication/password_reset_confirm.html', {'validlink': True, 'user': user})

            if len(password) < 6:
                messages.error(request, 'Password is too short.')
                return render(request, 'authentication/password_reset_confirm.html', {'validlink': True, 'user': user})

            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful. You can now log in with your new password.')
            return redirect('login')
        else:
            messages.error(request, 'The password reset link was invalid, possibly because it has already been used.')
            return redirect('password_reset_request')
