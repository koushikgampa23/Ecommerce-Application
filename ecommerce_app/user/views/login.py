from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.validators import ValidationError
from ..models import CustomUser
from .utils import generate_token


# Create your views here.
class Login(APIView):
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        if email is None or password is None:
            raise ValidationError({"error": "Please Fill all fields(email, password)"})

        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise ValidationError({"error": "No userfound, Please Register"})

        if user.check_password(password):
            access_token, refresh_token = generate_token(user)
            response = Response({"message": "Logged In successfull"})
            response.set_cookie("accessToken", access_token)
            response.set_cookie("refreshToken", refresh_token)
            return response
        else:
            raise ValidationError({"error": "Please Check your password"})

        return Response({"message": "User has been created"}, 201)
