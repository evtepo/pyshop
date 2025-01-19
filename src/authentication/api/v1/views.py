from datetime import datetime, UTC

import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from authentication.api.v1.serializers import AuthJWTSerializer, UserSerializer, RegisterUserSerializer
from authentication.models import CustomUser, RefreshToken


class RegisterView(APIView):
    def post(self, request: Request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request: Request):
        try:
            refrest_token = request.data.get("refresh_token")
            token = RefreshToken.objects.filter(id=refrest_token).first()
            token.expire = True
            token.save()
            return Response({"success": "User logged out."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"msg": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
        user = request.user
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = AuthJWTSerializer(data=request.data)
        if serializer.is_valid():
            user: CustomUser = serializer.validated_data.get("user")
            email = user.email
            access_token = jwt.encode(
                {
                    "sub": email,
                    "iat": datetime.now(UTC),
                    "exp": datetime.now(UTC) + settings.ACCESS_EXPIRE,
                },
                settings.SECRET_KEY,
                algorithm="HS256",
            )

            refresh_token = RefreshToken(user=user, exp_time=datetime.now() + settings.REFRESH_EXPIRE)
            refresh_token.save()
            data = {
                "access_token": access_token,
                "refresh_token": refresh_token.id,
            }

            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    ...
