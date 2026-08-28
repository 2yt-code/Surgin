from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from device_tracker.models import Device
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    TokenRefreshSerializer,
)

from typing import Dict, Any
from apps.v1.account.models import FingerPrint
import utils


User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        request = self.context.get('request')
        refresh = self.get_token(self.user)
        device_info = utils.device_info.get(
            request, 
            request.META.get('HTTP_USER_AGENT')
        )

        user_agent = device_info.get('user_agent')
        browser = device_info.get('browser')
        platform = device_info.get('platform')
        device_type = device_info.get('device_type')
        key = utils.fingerprint.create(f'{user_agent}:{browser}:{platform}:{device_type}')

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        device_tracker = utils.custom_device_tracker.track_device(
            request,
            self.user,
            refresh
        )
        FingerPrint.objects.create(
            device=device_tracker,
            key=key,
        ).save()

        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except AttributeError:
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)

        try:
            request = self.context.get('request')
            device_info = utils.device_info.get(
                request,
                request.META.get('HTTP_USER_AGENT')
            )

            user_agent = device_info.get('user_agent')
            browser = device_info.get('browser')
            platform = device_info.get('platform')
            device_type = device_info.get('device_type')
            key = utils.fingerprint.create(f'{user_agent}:{browser}:{platform}:{device_type}')

            fingerprint = FingerPrint.objects.filter(key=key).first()
            if fingerprint:
                fingerprint.last_verified_at = timezone.now()
                # TODO Architectural Design: User credential value and its impact on authentication
                if fingerprint.trust_score <=40: raise
                fingerprint.trust_score += 1
            else: raise

            device = Device.objects.get(pk=fingerprint.pk)
            if device:
                if not device.is_active: raise
                device.last_seen = timezone.now()
            else: raise

            fingerprint.save()
            device.save()

        except:
            raise exceptions.AuthenticationFailed(
                detail='Token is invalid or expired',
                code='token_not_valid'
            )
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
