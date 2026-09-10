from rest_framework import serializers


class SuccessResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()

class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

class ProfileResponseSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    premium = serializers.BooleanField()