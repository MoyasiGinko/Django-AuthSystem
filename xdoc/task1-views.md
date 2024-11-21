#### Overview (Authentication app)

The authentication system handles user registration, login, email verification, password reset, and account activation. The following views and functions are implemented:

1. **Email and Username Validation**
2. **User Registration**
3. **Account Verification**
4. **User Login and Logout**
5. **Profile View**
6. **Account Activation and Resending Activation Email**
7. **Password Reset Request and Confirmation**

---

### Views

#### 1. **EmailValidationView**

**Purpose:** Validates the email address format and checks if the email is already in use.

**Method:**

- `POST`: Accepts JSON data containing an email address. Returns a JSON response indicating whether the email is valid or already in use.

```python
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry, this email is in use. Please choose another one.'}, status=409)
        return JsonResponse({'email_valid': True})
```

#### 2. **UsernameValidationView**

**Purpose:** Validates the username format and checks if the username is already in use.

**Method:**

- `POST`: Accepts JSON data containing a username. Returns a JSON response indicating whether the username is valid or already in use.

```python
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry, this username is in use. Please choose another one.'}, status=409)
        return JsonResponse({'username_valid': True})
```

#### 3. **RegistrationView**

**Purpose:** Handles user registration by validating and saving user data.

**Method:**

- `GET`: Renders the registration form.
- `POST`: Processes the registration form, validates input, creates a new user, and sends an activation email.

```python
class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # Extract form data
        # Validate and create user
        # Send activation email and show success message
        ...
```

#### 4. **VerificationView**

**Purpose:** Handles account verification using a unique token.

**Method:**

- `GET`: Verifies the activation token and activates the user account.

```python
class VerificationView(View):
    def get(self, request, uidb64, token):
        # Verify token and activate account
        ...
```

#### 5. **LoginView**

**Purpose:** Handles user login.

**Method:**

- `GET`: Renders the login form.
- `POST`: Authenticates the user and logs them in.

```python
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        # Authenticate and log in user
        ...
```

#### 6. **LogoutView**

**Purpose:** Logs out the user.

**Method:**

- `POST`: Logs out the user and redirects to the login page.

```python
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('login')
```

#### 7. **ProfileView**

**Purpose:** Displays the logged-in user's profile.

**Method:**

- `GET`: Renders the profile page with user data.

```python
class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"user": request.user})
```

#### 8. **ActivationSuccessView**

**Purpose:** Renders a page indicating successful account activation.

**Method:**

- `GET`: Renders the activation success page.

```python
class ActivationSuccessView(View):
    def get(self, request):
        return render(request, 'authentication/activation_success.html')
```

#### 9. **ActivationInvalidView**

**Purpose:** Renders a page indicating an invalid activation link.

**Method:**

- `GET`: Renders the activation invalid page.

```python
class ActivationInvalidView(View):
    def get(self, request):
        return render(request, 'authentication/activation_invalid.html')
```

#### 10. **ActivationPromptView**

**Purpose:** Prompts the user to activate their account.

**Method:**

- `GET`: Renders the activation prompt page.

```python
class ActivationPromptView(View):
    def get(self, request, user_id):
        user = get_object_or_404(get_user_model(), id=user_id)
        return render(request, "authentication/activation_prompt.html", {"user": user})
```

#### 11. **ResendActivationEmailView**

**Purpose:** Resends the activation email to a user.

**Method:**

- `POST`: Resends the activation email if the account is not active.

```python
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
```

#### 12. **ActivateAccountView**

**Purpose:** Handles account activation requests.

**Method:**

- `GET`: Renders the account activation page.
- `POST`: Resends activation email or handles already activated account.

```python
class ActivateAccountView(View):
    def get(self, request):
        return render(request, 'authentication/activate_account.html')

    def post(self, request):
        # Handle activation request
        ...
```

#### 13. **PasswordResetRequestView**

**Purpose:** Handles password reset requests.

**Method:**

- `GET`: Renders the password reset request form.
- `POST`: Sends a password reset email if the email is associated with a user.

```python
class PasswordResetRequestView(View):
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, 'authentication/password_reset_request.html', {'form': form})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            # Send password reset email
            ...
```

#### 14. **PasswordResetConfirmView**

**Purpose:** Handles password reset confirmation and updating.

**Method:**

- `GET`: Renders the password reset confirmation page.
- `POST`: Updates the user's password if the link is valid and the passwords match.

```python
class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        # Render reset confirmation page
        ...

    def post(self, request, uidb64, token):
        # Update user's password
        ...
```

---

### Utility Functions

#### **send_activation_email**

**Purpose:** Sends an account activation email to the user.

**Parameters:**

- `request`: The HTTP request object.
- `user`: The user object to whom the email is sent.

```python
def send_activation_email(request, user):
    ...
```

---

### Forms

#### **PasswordResetRequestForm**

**Purpose:** Handles the form for requesting a password reset.

```python
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="Enter your email",
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
```

---

### Key Points

- **Validation:** Email and username validations ensure that input meets specified criteria and is not already in use.
- **Registration:** Users are registered with additional information and receive an activation email.
- **Activation:** Users must activate their accounts through an email link.
- **Login/Logout:** Users can log in and out of their accounts.
- **Profile:** Users can view their profile information.
- **Password Reset:** Users can request and confirm password resets.
