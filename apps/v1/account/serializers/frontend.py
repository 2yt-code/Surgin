from typing import Dict, Any
from uuid import uuid4
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    TokenRefreshSerializer,
)

from apps.v1.account.models import FingerPrint, Device
from apps.v1.account.signals import (
    get_uuid, 
    get_user_agent, 
    login_account,
    get_client_ip,
    check_fingerprint,
    get_refresh_token
)
import utils


User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        request = self.context.get('request')
        key = utils.fingerprint.scheme_key(request)
        uuid = get_uuid(request)

        try:
            fingerprint = FingerPrint.objects.get(
                device__user=self.user.pk,
                key=key
            )
            if uuid:
                if not fingerprint.device.uuid == uuid:
                    raise exceptions.AuthenticationFailed(_('Authentication failed'))
                data['uuid'] = uuid
            
            else:
                data['uuid'] = fingerprint.device.uuid

            login_valid = login_account(request, uuid=data.get('uuid'))
            if not login_valid: 
                raise exceptions.AuthenticationFailed(_('Authentication failed'))

        except FingerPrint.DoesNotExist:
            device_model = Device.objects.create(
                uuid=uuid4().hex,
                user=self.user,
                ip_address=get_client_ip(request),
                device_name=get_user_agent(request)
            )
            FingerPrint.objects.create(
                device=device_model,
                key=key
            )
            data['uuid'] = device_model.uuid

        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField(required=False)

    def validate(self, attrs):
        request = self.context.get('request')
        refresh_cookie = get_refresh_token(request)
        if not refresh_cookie:
            refresh_cookie = attrs.get('refresh')

        request = self.context.get('request')
        fingerprint = check_fingerprint(request, uuid=get_uuid(request))
        if not fingerprint: 
            raise exceptions.AuthenticationFailed(
                detail=_('Token is invalid or expired'),
                code='token_not_valid'
            )
        
        refresh = self.token_class(refresh_cookie)
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
