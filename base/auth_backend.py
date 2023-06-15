from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import User


class PhoneEmailAuthenticate(ModelBackend):
    def authenticate(self, request, username=None, password=None):

        if username.isdigit():
            try:
                user = User.objects.get(phone=username)
            except User.DoesNotExist:
                return None
        else:
            try:    
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password):
            return user
