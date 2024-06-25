import jwt
from django.conf import settings
from datetime import datetime, timedelta
from ..models import OutstandingTokens


def insert_token(user, access_token, refresh_token, expiry_date, refresh_expiry_date):
    token = OutstandingTokens.objects.create(
        user=user, type="accessToken", token=access_token, expiry=expiry_date
    )
    token.save()
    token = OutstandingTokens.objects.create(
        user=user, type="refreshToken", token=refresh_token, expiry=refresh_expiry_date
    )
    token.save()


def generate_token(user):
    key = settings.SECRET_KEY
    expiry_date = datetime.now() + timedelta(minutes=10)
    expiry_date_seconds = expiry_date.timestamp()
    refresh_expiry_date = datetime.now() + timedelta(minutes=60)
    refresh_expiry_date_seconds = refresh_expiry_date.timestamp()
    encode_jwt = jwt.encode(
        {"id": user.id, "iss": "django_app", "exp": expiry_date_seconds},
        key,
        algorithm="HS256",
    )
    refresh_jwt = jwt.encode(
        {"id": user.id, "iss": "django_app", "exp": refresh_expiry_date_seconds},
        key,
        algorithm="HS256",
    )
    insert_token(user, encode_jwt, refresh_jwt, expiry_date, refresh_expiry_date)
    return (encode_jwt, refresh_jwt)
