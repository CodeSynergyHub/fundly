from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from utils import decode_jwt


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None  # Return None if there's no auth header

        try:
            token = auth_header.split(' ')[1]
            payload = decode_jwt(token, secret_key=settings.SECRET_KEY)
            user = User(id=int(payload.get("id")), username=payload.get("username"))
            return user, None
        except (IndexError, ValueError):
            raise AuthenticationFailed('Invalid Token')
