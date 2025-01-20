from uuid import UUID

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from authentication.api.v1.serializers import AuthJWTSerializer, UserSerializer, RegisterUserSerializer
from authentication.models import CustomUser, RefreshToken
from authentication.utils import obtain_pair_tokens


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
            data = obtain_pair_tokens(user)

            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        try:
            UUID(refresh_token, version=4)
        except ValueError:
            return Response({"msg": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST) 

        check_token = RefreshToken.objects.filter(id=refresh_token, expire=False).first()
        if not check_token:
            return Response({"msg": "Invalid token or token time expired."}, status=status.HTTP_400_BAD_REQUEST)

        expired_token = RefreshToken.objects.get(id=refresh_token)
        expired_token.delete()

        data = obtain_pair_tokens(check_token.user)

        return Response(data, status=status.HTTP_200_OK)
