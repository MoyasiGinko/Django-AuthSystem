from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
            # Return the user without checking the password
            return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
