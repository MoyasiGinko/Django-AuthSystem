## Overview settings.py

### `INSTALLED_APPS`

- **Purpose:** This list includes all the applications that are enabled in your Django project.
- **Components:**
  - `'authentication'`: Your custom app for handling user authentication.
  - `'realestate'`: Your custom app for managing real estate-related functionality.

### `EMAIL_BACKEND`

- **Purpose:** Specifies the backend used to send emails.
- **Value:** `'django.core.mail.backends.smtp.EmailBackend'` configures Django to use SMTP (Simple Mail Transfer Protocol) for sending emails.

### `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`

- **Purpose:** These settings configure the email server and credentials.
  - **`EMAIL_HOST`:** The SMTP server to connect to (e.g., `'smtp.gmail.com'` for Gmail).
  - **`EMAIL_PORT`:** The port used for the SMTP connection (587 for TLS).
  - **`EMAIL_USE_TLS`:** Whether to use TLS (Transport Layer Security) for the connection (`True` for secure connections).
  - **`DEFAULT_FROM_EMAIL`:** The default email address used for sending emails.
  - **`EMAIL_HOST_USER`:** The email account used for authentication with the SMTP server.
  - **`EMAIL_HOST_PASSWORD`:** The password for the email account.

### `AUTH_USER_MODEL`

- **Purpose:** Specifies the custom user model to use in your project.
- **Value:** `'authentication.CustomUser'` tells Django to use the `CustomUser` model from the `authentication` app instead of the default user model.

### `MEDIA_URL`, `MEDIA_ROOT`

- **Purpose:** These settings manage media files (uploaded files).
  - **`MEDIA_URL`:** The URL that handles media files served from `MEDIA_ROOT` (e.g., `/media/`).
  - **`MEDIA_ROOT`:** The filesystem path where uploaded media files are stored (e.g., `BASE_DIR / 'media'`).

### `LOGOUT_REDIRECT_URL`

- **Purpose:** Defines where users are redirected after logging out.
- **Value:** `'login'` specifies that users should be redirected to the login page after they log out.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'realestate',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

AUTH_USER_MODEL = 'authentication.CustomUser'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGOUT_REDIRECT_URL = 'login'
```

**Notes:**

- Use environment variables for sensitive information (`SECRET_KEY`, database credentials, email settings).
- Adjust `ALLOWED_HOSTS`, `DATABASES`, and other settings as needed based on your production environment.

## Overview urls.py

### `urlpatterns`

- **`path('admin/', admin.site.urls)`**: Routes URLs starting with `admin/` to the Django admin site.
- **`path('', include('realestate.urls'))`**: Includes URL patterns from the `realestate` app. This means that any URL starting from the root will be routed to the `realestate` app’s URL configuration.
- **`path('authentication/', include('authentication.urls'))`**: Includes URL patterns from the `authentication` app. This means that URLs starting with `authentication/` will be routed to the `authentication` app’s URL configuration.

### `if settings.DEBUG:`

- **`urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`**: This line ensures that during development (when `DEBUG` is `True`), Django serves media files from the `MEDIA_ROOT` directory at the URL specified by `MEDIA_URL`. This is useful for handling user-uploaded files during development but should be configured differently in a production environment (typically by serving media files through a web server like Nginx or Apache)
