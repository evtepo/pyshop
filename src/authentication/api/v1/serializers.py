from django.contrib.auth import authenticate
from rest_framework import serializers

from authentication.models import CustomUser


class RefreshTokenMixin(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)


class UserMixin(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email")


class UserSerializer(UserMixin): ...


class UserUpdateSerializer(UserMixin):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)


class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, default=None)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
        )
        user.set_password(validated_data.get("password"))
        user.save()

        return user
    

class AuthJWTSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email, password = attrs.get("email"), attrs.get("password")
        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        attrs["user"] = user

        return attrs


class LogoutSerializer(RefreshTokenMixin): ...


class RefreshTokenSerializer(RefreshTokenMixin): ...
