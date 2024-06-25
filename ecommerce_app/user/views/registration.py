from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.validators import ValidationError
from ..models import CustomUser


# Create your views here.
class Registration(APIView):
    authentication_classes = []

    def post(self, request):
        username = request.data.get("username", None)
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if username is None or email is None or password is None:
            raise ValidationError(
                {"error": "Please Fill all fields(username, email, password)"}
            )

        is_username = CustomUser.objects.filter(username=username).exists()
        if is_username:
            raise ValidationError({"error": "Username already exists"})

        is_email = CustomUser.objects.filter(email=email).exists()
        if is_email:
            raise ValidationError({"error": "email already exists"})

        user = CustomUser.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return Response({"message": "User has been created"}, 201)
