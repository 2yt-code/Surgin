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