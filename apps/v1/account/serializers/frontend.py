from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from typing import Dict, Any
from apps.v1.account.models import FingerPrint
import utils


User = get_user_model()

class CustomTokenObtainSerializer(TokenObtainSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        try:
            user = User.objects.get(username=attrs.get(self.username_field))
            fingerprint_user = FingerPrint.objects.get(user_id=user.id)
        except:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account"
            )

        try:
            request = self.context.get('request')
            self.user = authenticate(**authenticate_kwargs)
                        
            if utils.fingerprint.compare(request.META.get('HTTP_USER_AGENT'), fingerprint_user.user_agent):
                if request.META.get('REMOTE_ADDR') == fingerprint_user.ip_address or fingerprint_user.trust_level >= 40:
                    fingerprint_user.trust_level += 10
                    fingerprint_user.save()
                else: raise
            else: raise

        except:
            if fingerprint_user:
                fingerprint_user.trust_level -= 10
                fingerprint_user.save()
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account"
            )
        
        return {}

class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class RegisterSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).first():
            raise serializers.ValidationError({'email': _('Email already exists')})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username', 
            'email', 
            'password'
            ]
        
        extra_kwrags = {
            'password': {'write_only': True}
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username', 
            'email',
            'premium'
        ]
