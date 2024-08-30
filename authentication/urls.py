from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import (
    RegistrationView,
    UsernameValidationView,
    EmailValidationView,
    LogoutView,
    VerificationView,
    LoginView,
    ActivationSuccessView,
    ActivationInvalidView,
    ResendActivationEmailView,
    ActivationPromptView,
    ActivateAccountView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ProfileView,

)

urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate_email'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('activation-success/', ActivationSuccessView.as_view(), name='activation_success'),
    path('activation-invalid/', ActivationInvalidView.as_view(), name='activation_invalid'),
    path('resend-activation-email/', ResendActivationEmailView.as_view(), name='resend_activation_email'),
    path('activation-prompt/<int:user_id>/', ActivationPromptView.as_view(), name='activation_prompt'),
    path('activate-account/', ActivateAccountView.as_view(), name='activate_account'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
