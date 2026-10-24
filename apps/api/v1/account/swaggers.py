from rest_framework import serializers
from django_countries.fields import CountryField

class SchemaResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()

class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

class UserResponseSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    premium = serializers.BooleanField()
    language = CountryField()

class PasswordResetResponse(serializers.Serializer):
    status = serializers.CharField()

class PasswordResetErrorResponse(serializers.Serializer):
    detail = serializers.CharField()