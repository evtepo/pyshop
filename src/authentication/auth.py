import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from authentication.models import CustomUser


class JWTAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def authenticate_credentials(self, key):
        try:
            payload = jwt.decode(key, settings.SECRET_KEY, algorithms=["HS256"])
            user = CustomUser.objects.get(email=payload["sub"])
        except (jwt.DecodeError, CustomUser.DoesNotExist):
            raise exceptions.AuthenticationFailed("Invalid token.")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired.")
        if not user.is_active:
            raise exceptions.AuthenticationFailed("User inactive or deleted.")

        return (user, payload)
