from jwt import decode
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication


class CustomAuth(BaseAuthentication):
    """
    All authentication classes should extend BaseAuthentication.
    """

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        token = request.COOKIES.get("token", None)
        if token is None:
            raise AuthenticationFailed("token invalid, failed here")
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        """Checks user valid or not"""
        try:
            decoded_jwt = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_jwt.get("id", None)
            user_obj = get_user_model().objects.get(id=user_id)
            return (user_obj, token)
        except:
            raise AuthenticationFailed("Token is invalid")
