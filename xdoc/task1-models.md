## Models (Authentication app)

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator

class CustomUser(AbstractUser):
    username = models.CharField(max_length=10, unique=True)  # Ensure username is unique
    password = models.CharField(max_length=128, validators=[MinLengthValidator(8)])  # Corrected password field
    company_name = models.CharField(max_length=30, blank=True, null=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    province_code = models.CharField(max_length=2, blank=True, null=True)
    area_code = models.CharField(max_length=4, blank=True, null=True)
    address = models.CharField(max_length=30, blank=True, null=True)
    phone1 = models.CharField(max_length=15, blank=True, null=True)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    registration_date = models.DateField(auto_now_add=True)
    current_activation_date = models.DateField(blank=True, null=True)
    expiry_current_activation = models.DateField(blank=True, null=True)
    subscription_type = models.CharField(max_length=1, choices=[('F', 'Free'), ('P', 'Paid')], default='F')
    mem_activation_status = models.CharField(max_length=1, choices=[('A', 'Active'), ('I', 'Inactive')], default='I')
    note_and_description = models.TextField(blank=True, null=True)
```

### 1. **username**

- **Type:** `CharField`
- **Max Length:** 10
- **Unique:** Yes
- **Description:** The username for the user. It must be unique across the system.

### 2. **password**

- **Type:** `CharField`
- **Max Length:** 128
- **Validators:** `MinLengthValidator(8)`
- **Description:** The password for the user, with a minimum length of 8 characters. Note that Django’s `AbstractUser` already includes a password field, but if you want to override it, ensure the custom implementation is consistent with security best practices.

### 3. **company_name**

- **Type:** `CharField`
- **Max Length:** 30
- **Blank:** Yes
- **Null:** Yes
- **Description:** The name of the company associated with the user. This field is optional.

### 4. **company_logo**

- **Type:** `ImageField`
- **Upload To:** `company_logos/`
- **Blank:** Yes
- **Null:** Yes
- **Description:** An image field for the company logo. If not provided, the field will be blank.

### 5. **province_code**

- **Type:** `CharField`
- **Max Length:** 2
- **Blank:** Yes
- **Null:** Yes
- **Description:** A code representing the province or state. This field is optional.

### 6. **area_code**

- **Type:** `CharField`
- **Max Length:** 4
- **Blank:** Yes
- **Null:** Yes
- **Description:** A code representing the area or region. This field is optional.

### 7. **address**

- **Type:** `CharField`
- **Max Length:** 30
- **Blank:** Yes
- **Null:** Yes
- **Description:** The address associated with the user. This field is optional.

### 8. **phone1**

- **Type:** `CharField`
- **Max Length:** 15
- **Blank:** Yes
- **Null:** Yes
- **Description:** Primary phone number for the user. This field is optional.

### 9. **phone2**

- **Type:** `CharField`
- **Max Length:** 15
- **Blank:** Yes
- **Null:** Yes
- **Description:** Secondary phone number for the user. This field is optional.

### 10. **email**

- **Type:** `EmailField`
- **Blank:** Yes
- **Null:** Yes
- **Description:** Email address for the user. This field is optional.

### 11. **registration_date**

- **Type:** `DateField`
- **Auto Now Add:** Yes
- **Description:** The date when the user registered. This field is automatically set to the current date when the user is created.

### 12. **current_activation_date**

- **Type:** `DateField`
- **Blank:** Yes
- **Null:** Yes
- **Description:** The date when the user’s account was activated. This field is optional.

### 13. **expiry_current_activation**

- **Type:** `DateField`
- **Blank:** Yes
- **Null:** Yes
- **Description:** The date when the current activation period will expire. This field is optional.

### 14. **subscription_type**

- **Type:** `CharField`
- **Max Length:** 1
- **Choices:**
  - `('F', 'Free')`
  - `('P', 'Paid')`
- **Default:** `F`
- **Description:** Indicates the subscription type of the user. Defaults to "Free".

### 15. **mem_activation_status**

- **Type:** `CharField`
- **Max Length:** 1
- **Choices:**
  - `('A', 'Active')`
  - `('I', 'Inactive')`
- **Default:** `I`
- **Description:** Indicates the activation status of the user's membership. Defaults to "Inactive".

### 16. **note_and_description**

- **Type:** `TextField`
- **Blank:** Yes
- **Null:** Yes
- **Description:** A field for additional notes and descriptions. This field is optional.

## Notes

1. **Password Handling:**

   - Django’s default `AbstractUser` class includes a password field with proper hashing and validation. Overriding this field might require additional changes to ensure compatibility with Django's authentication system. If you don’t need a custom password field, it’s recommended to use the built-in password handling.

2. **Image Handling:**

   - Make sure you have the appropriate media settings configured in your Django project to handle file uploads and serve media files.

3. **Validation:**
   - Ensure to add necessary validators or custom validation logic if required, especially if overriding fields with custom logic.

---
