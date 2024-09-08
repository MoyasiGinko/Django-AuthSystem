## Overview _urls.py_ (Authentication app)

```python
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
```

### 1. **EmailValidationView**

- **URL:** `/validate-email`
- **Method:** `POST`
- **Purpose:** Validates the email address provided by the user.
- **Responses:**
  - `200 OK`: Email is valid.
  - `400 Bad Request`: Email is invalid.
  - `409 Conflict`: Email is already in use.

### 2. **UsernameValidationView**

- **URL:** `/validate-username`
- **Method:** `POST`
- **Purpose:** Validates the username provided by the user.
- **Responses:**
  - `200 OK`: Username is valid.
  - `400 Bad Request`: Username contains non-alphanumeric characters.
  - `409 Conflict`: Username is already in use.

### 3. **RegistrationView**

- **URL:** `/register`
- **Method:** `GET`, `POST`
- **Purpose:** Handles user registration.
- **POST Data:**
  - `username`, `email`, `password`, `companyname`, `provincecode`, `areacode`, `address`, `phone1`, `phone2`, `noteandescription`, `company_logo`
- **Responses:**
  - On success: Redirects to activation prompt and sends an activation email.
  - On failure: Displays error messages and re-renders the registration form.

### 4. **VerificationView**

- **URL:** `/activate/<uidb64>/<token>`
- **Method:** `GET`
- **Purpose:** Activates the user account using the provided token.
- **Responses:**
  - On success: Redirects to activation success page.
  - On failure: Redirects to activation invalid page.

### 5. **LoginView**

- **URL:** `/login`
- **Method:** `GET`, `POST`
- **Purpose:** Handles user login.
- **POST Data:**
  - `username`, `password`
- **Responses:**
  - On success: Redirects to the user profile.
  - On failure: Displays error messages and re-renders the login form.

### 6. **LogoutView**

- **URL:** `/logout`
- **Method:** `POST`
- **Purpose:** Logs out the user and redirects to the login page.
- **Responses:** Redirects to login page with a success message.

### 7. **ProfileView**

- **URL:** `/profile`
- **Method:** `GET`
- **Purpose:** Displays the logged-in user's profile.
- **Responses:** Renders the user's profile page.

### 8. **ActivationSuccessView**

- **URL:** `/activation-success/`
- **Method:** `GET`
- **Purpose:** Displays a success message after account activation.
- **Responses:** Renders activation success page.

### 9. **ActivationInvalidView**

- **URL:** `/activation-invalid/`
- **Method:** `GET`
- **Purpose:** Displays an error message for invalid activation links.
- **Responses:** Renders activation invalid page.

### 10. **ResendActivationEmailView**

- **URL:** `/resend-activation-email/`
- **Method:** `POST`, `GET`
- **Purpose:** Resends the activation email to the user.
- **POST Data:**
  - `user_id`
- **Responses:**
  - On success: Redirects to the activation prompt with a message.
  - On failure: Redirects to the activation prompt.

### 11. **ActivationPromptView**

- **URL:** `/activation-prompt/<int:user_id>/`
- **Method:** `GET`
- **Purpose:** Displays a prompt for the user to activate their account.
- **Responses:** Renders activation prompt page.

### 12. **ActivateAccountView**

- **URL:** `/activate-account/`
- **Method:** `GET`, `POST`
- **Purpose:** Handles activation of accounts based on email.
- **POST Data:**
  - `email`
- **Responses:**
  - On success: Sends activation email if the account is not already active.
  - On failure: Displays an error message.

### 13. **PasswordResetRequestView**

- **URL:** `/password-reset/`
- **Method:** `GET`, `POST`
- **Purpose:** Handles password reset requests.
- **POST Data:**
  - `email`
- **Responses:**
  - On success: Sends a password reset email.
  - On failure: Displays an error message.

### 14. **PasswordResetConfirmView**

- **URL:** `/password-reset-confirm/<uidb64>/<token>/`
- **Method:** `GET`, `POST`
- **Purpose:** Confirms and resets the password using the provided token.
- **POST Data:**
  - `password`, `password_confirm`
- **Responses:**
  - On success: Resets the password and redirects to the login page.
  - On failure: Displays error messages and re-renders the reset form.

## URL Patterns

The `urlpatterns` list defines the URL routes for the views:

- **`/register`** - Registration page.
- **`/login`** - Login page.
- **`/logout`** - Logs out the user.
- **`/validate-username`** - Validates the username.
- **`/validate-email`** - Validates the email.
- **`/activate/<uidb64>/<token>`** - Activates the user account.
- **`/profile`** - User profile page.
- **`/activation-success/`** - Activation success page.
- **`/activation-invalid/`** - Activation invalid page.
- **`/resend-activation-email/`** - Resends activation email.
- **`/activation-prompt/<int:user_id>/`** - Activation prompt page.
- **`/activate-account/`** - Activates account using email.
- **`/password-reset/`** - Password reset request page.
- **`/password-reset-confirm/<uidb64>/<token>/`** - Password reset confirmation page.

---
