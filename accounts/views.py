from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .tokens import account_activation_token
from django.urls import reverse
from django.http import HttpResponse




def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set account to inactive until activation
            user.save()
            # Redirect to activation prompt with user ID
            return redirect('activation_prompt', user_id=user.id)
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})



def activation_prompt(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    return render(request, "accounts/activation_prompt.html", {"user": user})



def send_activation_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    message = render_to_string('accounts/activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'activation_link': reverse('activate_account', kwargs={
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

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(get_user_model(), pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'accounts/activation_success.html')
    else:
        return render(request, 'accounts/activation_invalid.html')


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("dashboard")
                else:
                    # Account is inactive; show a message and a link to request activation
                    messages.error(request, "Your account is not activated.")
                    return render(request, "accounts/login.html", {
                        "form": form,
                        "user_id": user.id
                    })
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def dashboard(request):
    return render(request, "accounts/dashboard.html", {"user": request.user})

def activation_prompt(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    return render(request, "accounts/activation_prompt.html", {"user": user})



def resend_activation_email(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user = get_object_or_404(get_user_model(), id=user_id)
        if not user.is_active:
            send_activation_email(request, user)
            messages.info(request, "Activation email sent. Please check your inbox.")
        else:
            messages.info(request, "Account is already activated.")
        return redirect('activation_prompt', user_id=user_id)  # Pass user_id here
    return redirect('activation_prompt')


def logout_view(request):
    logout(request)
    return redirect('login')


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
    return render(request, 'accounts/activate_account.html')