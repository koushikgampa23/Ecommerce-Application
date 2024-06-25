from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=10)
    location = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    role = models.CharField(max_length=30)


class OutstandingTokens(models.Model):
    """Storing the tokens that has been generated"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField()
    token = models.CharField()
    expiry = models.DateTimeField()


class BlackListedTokens(models.Model):
    """Black Listing the tokens that has been logged out, Token foreignkey of outstanding, blacklisted time"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField()
    token = models.CharField()
