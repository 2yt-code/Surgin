from typing import Dict, Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import (
    serializers, 
    exceptions, 
)
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    TokenRefreshSerializer,
)

from apps.api.v1.account.constants import RESERVED_NAMES
from apps.api.v1.core.artist.serializers import ArtistBasicInformationSerializer
from apps.api.v1.core.playlist.models import Playlist
from apps.api.v1.core.track.serializers import TrackBasicInformationSerializer
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
        from apps.api.v1.account.services import get_device_id, login_account
        data = super().validate(attrs)
        request = self.context.get('request')
        key = utils.fingerprint.scheme_key(request)
        device_id = get_device_id(request)
        login_user_data = login_account(
            user=self.user,
            key=key,
            device_id=device_id,
            request=request,
            data=data
        )
        refresh = self.get_token(self.user)
        login_user_data['refresh'] = str(refresh)
        login_user_data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return login_user_data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField(required=False)

    def validate(self, attrs):
        from apps.api.v1.account.services import (
            get_refresh_token, 
            check_fingerprint, 
            get_device_id
        )

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
        from apps.api.v1.account.services import create_user_account
        
        user = create_user_account(**validated_data)
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

class UserBasicInformationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    username = serializers.CharField()

class UserFollowingsRetrieveSerializer(serializers.Serializer):
    artist = serializers.SerializerMethodField()

    def get_artist(self, obj):
        artist = obj.artist
        return ArtistBasicInformationSerializer(instance=artist).data
    
class UserFollowingsCreateSerializer(serializers.Serializer):
    artist_id = serializers.UUIDField()

class UserPlaylistByIDRetrieveSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    collaborators = serializers.SerializerMethodField()
    tracks = serializers.SerializerMethodField()

    def get_owner(self, obj):
        user = obj.owner
        return UserBasicInformationSerializer(instance=user).data

    def get_collaborators(self, obj):
        users = obj.collaborators.all()
        return UserBasicInformationSerializer(instance=users, many=True).data

    def get_tracks(self, obj):
        tracks = obj.tracks.all()
        return TrackBasicInformationSerializer(instance=tracks, many=True).data

    class Meta:
        model = Playlist
        fields = [
            'id', 
            'name',
            'description',
            'baner',
            'owner',
            'collaborators',
            'tracks'
        ]

class UserPlaylistByIDUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = [
            'name',
            'description',
            'baner',
            'is_public'
        ]

class UserPlaylistsRetrieveSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    collaborators = serializers.SerializerMethodField()
    tracks = serializers.SerializerMethodField()

    def get_owner(self, obj):
        user = obj.owner
        return UserBasicInformationSerializer(instance=user).data

    def get_collaborators(self, obj):
        users = obj.collaborators.all()
        return UserBasicInformationSerializer(instance=users, many=True).data

    def get_tracks(self, obj):
        tracks = obj.tracks.all()
        return TrackBasicInformationSerializer(instance=tracks, many=True).data

    class Meta:
        model = Playlist
        fields = [
            'id',
            'owner',
            'collaborators',
            'name',
            'description',
            'baner',
            'tracks'
        ]

class UserPlaylistTrackByIDCreateSerializer(serializers.Serializer):
    track_id = serializers.UUIDField()

class UserPlaylistCreateSerializer(serializers.Serializer): # TODO
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=300)
    baner = serializers.ImageField()

class UserActivationAccountSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=40)
    uid = serializers.CharField()

class UserRestoreAccountSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=40)
    uid = serializers.CharField()

class UserSendEmailRestoreAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
