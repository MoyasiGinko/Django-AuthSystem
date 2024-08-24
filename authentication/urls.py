from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
    RegistrationView,
    UsernameValidationView,
    EmailValidationView,
    LogoutView,
    VerificationView,
    LoginView,
    DashboardView,
    ActivationSuccessView,
    ActivationInvalidView,
    resend_activation_email,
    activation_prompt,
    activate_account_page,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate_email'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('activation-success/', ActivationSuccessView.as_view(), name='activation_success'),
    path('activation-invalid/', ActivationInvalidView.as_view(), name='activation_invalid'),
    path('resend-activation/', resend_activation_email, name='resend_activation'),
    path('activation-prompt/<int:user_id>/', activation_prompt, name='activation_prompt'),
    path('activate-account/', activate_account_page, name='activate_account'),
    path('resend-activation-email/', resend_activation_email, name='resend_activation_email'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
