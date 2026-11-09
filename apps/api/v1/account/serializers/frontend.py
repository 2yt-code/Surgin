from typing import Dict, Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import (
    serializers, 
    exceptions, 
    status
)
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    TokenRefreshSerializer,
)

from apps.api.v1.account.models import FingerPrint, Device
from apps.api.v1.account.constants import RESERVED_NAMES
from apps.api.v1.account.services import (
    get_device_id, 
    get_user_agent, 
    login_account,
    get_client_ip,
    check_fingerprint,
    get_refresh_token
)
from apps.api.v1.core.album.models import Album
from apps.api.v1.core.artist.models import Artist, ArtistFollow
from apps.api.v1.core.playlist.models import Playlist
import utils


User = get_user_model()

class CustomTokenObtainSerializer(TokenObtainSerializer):
    default_error_messages = {
        'no_active_account': _('Login failed'),
        'login_failed': _('Login failed')
    }

class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        request = self.context.get('request')
        key = utils.fingerprint.scheme_key(request)
        device_id = get_device_id(request)

        try:
            fingerprint = FingerPrint.objects.get(
                device__user=self.user.pk,
                key=key
            )
            if device_id:
                if not fingerprint.device.pk == device_id:
                    fingerprint.trust_score -= 1
                    fingerprint.save(update_fields=['trust_score'])
                    raise exceptions.AuthenticationFailed(
                        detail=self.default_error_messages['login_failed'],
                        code='login_failed'
                    )
                
                data['device_id'] = device_id
            else:
                data['device_id'] = fingerprint.device.pk

            login_valid = login_account(
                request, 
                user=self.user, 
                device_id=data.get('device_id')
            )
            if not login_valid: 
                fingerprint.trust_score -= 1
                fingerprint.save(update_fields=['trust_score'])
                raise exceptions.AuthenticationFailed(
                    detail=self.default_error_messages['login_failed'],
                    code='login_failed'
                )

        except FingerPrint.DoesNotExist:
            try:
                with transaction.atomic():
                    device_model = Device.objects.create(
                        user=self.user,
                        ip_address=get_client_ip(request),
                        device_name=get_user_agent(request)
                    )
                    FingerPrint.objects.create(
                        device=device_model,
                        key=key
                    )
                    data['device_id'] = device_model.pk
            except:
                fingerprint.trust_score -= 1
                fingerprint.save(update_fields=['trust_score'])
                raise exceptions.AuthenticationFailed(
                    detail=self.default_error_messages['login_failed'],
                    code='login_failed'
                )

        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField(required=False)

    def validate(self, attrs):
        request = self.context.get('request')
        refresh_token = get_refresh_token(request)
        if not refresh_token:
            refresh_token = attrs.get('refresh')

        fingerprint = check_fingerprint(
            request, 
            device_id=get_device_id(request)
        )
        if not fingerprint: 
            raise exceptions.AuthenticationFailed(
                detail=_('Token is invalid or expired'),
                code='token_not_valid'
            )
        
        refresh = self.token_class(refresh_token)
        data = {'access': str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    refresh.blacklist()
                except AttributeError:
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data['refresh'] = str(refresh)

        return data

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, 
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username', 
            'email', 
            'password',
            'language',
            'confirm_password'
            ]
        
        extra_kwrags = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['email'].strip().casefold() in RESERVED_NAMES:
            raise serializers.ValidationError(
                detail=_('This email is reserved'),
                code='email_reserved'
                )

        if data['username'].strip().casefold() in RESERVED_NAMES:
            raise serializers.ValidationError(
                detail=_('This username is reserved'),
                code='username_reserved'
            )

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                detail=_('This password must match'),
                code='password_must_match'
                )
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user
    
class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username', 
            'email',
            'language'
        ]

class UserFollowingsRetrieveSerializer(serializers.Serializer):
    artist = serializers.SlugRelatedField(
        read_only=True,
        slug_field='pk'
    )

class UserFollowingsCreateSerializer(serializers.Serializer):
    artist_id = serializers.UUIDField()

class UserPlaylistTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name'] # TODO

class UserPlaylistByIDRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name'] # TODO

class UserPlaylistByIDUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['name'] # TODO

class UserPlaylistsRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name'] # TODO

class UserPlaylistCreateSerializer(serializers.Serializer): # TODO
    name = serializers.CharField(
        max_length=50,
    )
    description = serializers.CharField(max_length=300)
    baner = serializers.ImageField()