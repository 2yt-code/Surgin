import uuid
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from rest_framework.request import Request
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.settings import api_settings
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample
)
from django_rest_passwordreset.views import (
    ResetPasswordValidateToken,
    ResetPasswordConfirm, 
    ResetPasswordRequestToken
)
from rest_framework import (
    status,
    generics,
    permissions,
    views,
)

from apps.api.v1.account.models import Device
from apps.api.v1.account.services import (
    check_id_format, 
    clear_auth_cookie, 
    create_paginator, 
    set_access_token, 
    set_auth_cookies
)
from apps.api.v1.account.swaggers import (
    SchemaResponseSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    UserResponseSerializer,
    PasswordResetResponse,
    PasswordResetErrorResponse
)
from apps.api.v1.account.serializers import (
    RegisterSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    UserFollowingsRetrieveSerializer,
    UserPlaylistsRetrieveSerializer,
    UserPlaylistByIDRetrieveSerializer,
    UserPlaylistCreateSerializer,
    UserPlaylistByIDUpdateSerializer,
    UserFollowingsCreateSerializer
)
from apps.api.v1.core.artist.models import Artist, ArtistFollow
from apps.api.v1.core.playlist.models import Playlist
from apps.api.v1.core.track.models import Track
import utils


User = get_user_model()

@extend_schema(
    tags=['User Authentication'],
    summary=_('Login to your account'),
    description=_('Authenticates the user and validates their device and fingerprint before issuing access and refresh tokens'),
    request=CustomTokenObtainPairSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenObtainPairResponseSerializer,
            description=_('Login successful'),
            examples=[
                OpenApiExample(
                    name=_('Login successful'),
                    value=dict(
                        access='access_token',
                        refresh='refresh_token'
                    ),
                    response_only=True
                )
            ]
        ),
        401: OpenApiResponse(
            response=SchemaResponseSerializer, 
            description=_('Login failed'),
            examples=[
                OpenApiExample(
                    name=_('No active user account found'),
                    value=dict(
                        detail=_('Login failed'),
                        code='no_active_account'
                    ),
                    response_only=True
                ),
                OpenApiExample(
                    name=_('Login failed'),
                    value=dict(
                        detail=_('Login failed'),
                        code='login_failed'
                    ),
                    response_only=True
                )
            ]
        ),
    }
)   
class CustomTokenObtainPairView(TokenViewBase):
    _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(
            dict(
                access=serializer.validated_data.get('refresh'), 
                refresh=serializer.validated_data.get('access')
            ), 
            status=status.HTTP_200_OK
        )

        device_model = Device.objects.get(pk=serializer.validated_data.get('device_id'))
        set_auth_cookies(
            response, 
            serializer.validated_data.get('access'),
            serializer.validated_data.get('refresh'),
            device_model
        )
        return response

@extend_schema(
    tags=['User Authentication'],
    summary=_('Reset access token'),
    description=_('Updates an expired access token using a valid refresh token'),
    request=CustomTokenRefreshSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenRefreshResponseSerializer,
            description=_('Token reset completed successfully'),
            examples=[
                OpenApiExample(
                    name=_('Token updated successfully'),
                    value=dict(
                        access=_('access_token'),
                    ),
                    response_only=True
                )
            ]
        ),
        401: OpenApiResponse(
            response=SchemaResponseSerializer,
            description=_('Token reset failed'),
            examples=[
                OpenApiExample(
                    name=_('Invalid refresh token'),
                    value=dict(
                        detail=_('Token is invalid or expired'),
                        code=_('token_not_valid')
                    ),
                    response_only=True
                )
            ]
        )
    }
)
class CustomTokenRefreshView(TokenViewBase):
    throttle_classes = (UserRateThrottle,)
    _serializer_class = api_settings.TOKEN_REFRESH_SERIALIZER

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        set_access_token(response, serializer.validated_data.get('access'))

        return response

@extend_schema(
    tags=['User Authentication'],
    summary=_('Create an account'),
    description=_('It creates a new user account using the provided registration information'),
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            description=_('Registration completed successfully'),
        ),
        500: OpenApiResponse(
            response=SchemaResponseSerializer,
            description=_('Registration was unsuccessful'),
            examples=[
                OpenApiExample(
                    name=_('Account registration failed'),
                    value=dict(
                        detail=_('Registration was unsuccessful'),
                        code='registration_failed'
                    ),
                    response_only=True
                )
            ]
        )
    }
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

@extend_schema(
    tags=['User Information'],
    summary=_('User account information'),
    description=_('Retrieves, Updates the authenticated users information'),
    request=UserSerializer,
    responses={
        200: OpenApiResponse(
            response=UserResponseSerializer,
            description=_('User information was successfully retrieved'),
            examples=[
                OpenApiExample(
                    name=_('Successful retrieval of user account information'),
                    value=dict(
                        first_name='user_firstname',
                        last_name='user_lastname',
                        username='user_username',
                        email='user_email',
                        premium='user_premium'
                    ),
                    response_only=True
                )
            ]
        ),
        401: OpenApiResponse(
            response=SchemaResponseSerializer,
            description=_('Failed to retrieve user information'),
            examples=[
                OpenApiExample(
                    name=_('Failed to retrieve user account information'),
                    value=dict(
                        detail=_('Authentication credentials were not provided.'),
                        code='not_authenticated'
                    ),
                    response_only=True
                )
            ]
        )
    }
)
class UserView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

@extend_schema(
    tags=['User Authentication'],
    summary=_('Logout account'),
    description=_('Invalidates the current refresh token and securely logs the user out'),
    responses={
        204: OpenApiResponse(
            description=_('Account logged out successfully'),
        ),
        500: OpenApiResponse(
            response=SchemaResponseSerializer,
            description=_('Failed to logout of the account'),
            examples=[
                OpenApiExample(
                    name=_('Account logout failed'),
                    value=dict(
                        detail=_('Logging out failed'),
                        code='logout_failed'
                    ),
                    response_only=True
                )
            ]
        )
    }
)
class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def post(self, request):
        key = utils.fingerprint.scheme_key(request)

        try:
            outstanding_tokens = OutstandingToken.objects.filter(
                user=request.user
            )
            for token in outstanding_tokens:
                BlacklistedToken.objects.get_or_create(
                    token=token
                )

            Device.objects.get(
                user=request.user, 
                fingerprint__key=key
            ).delete()

        except:
            return Response(
                dict(
                    detail=_('Failed to logout of the account'),
                    code='logout_failed'
                ), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        response = Response(status=status.HTTP_204_NO_CONTENT)
        clear_auth_cookie(response=response)
        return response

@extend_schema(tags=['User Authentication'])
class ChangePasswordView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data.get('new_password'))
        request.user.save(update_fields=['password'])
        return Response(status=status.HTTP_200_OK)
    
@extend_schema(
    tags=['User Authentication'],
    summary=_('Password reset token verification'),
    responses={
        200: OpenApiResponse(
            response=PasswordResetResponse,
            description=_('Password reset token is valid'),
            examples=[
                OpenApiExample(
                    name=_('Token is valid'),
                    value=dict(status='OK'),
                    response_only=True
                )
            ]
        ),
        404: OpenApiResponse(
            response=PasswordResetErrorResponse,
            description=_('Password reset token is invalid'),
            examples=[
                OpenApiExample(
                    name=_('Token is invalid'),
                    value=dict(detail='The OTP password entered is not valid. Please check and try again.'),
                    response_only=True
                )
            ]
        )
    }
)
class CustomResetPasswordValidateToken(ResetPasswordValidateToken):
    pass

@extend_schema(
    tags=['User Authentication'],
    summary=_('Confirm password reset'),
    responses={
        200: OpenApiResponse(
            response=PasswordResetResponse,
            description=_('Password reset successfully'),
            examples=[
                OpenApiExample(
                    name=_('Password reset successful'),
                    value=dict(status='OK'),
                    response_only=True
                )
            ]
        ),
        404: OpenApiResponse(
            response=PasswordResetErrorResponse,
            description=_('Password reset failed'),
            examples=[
                OpenApiExample(
                    name=_('Password reset failed'),
                    value=dict(detail='The OTP password entered is not valid. Please check and try again.'),
                    response_only=True
                )
            ]
        )
    }
)
class CustomResetPasswordConfirm(ResetPasswordConfirm):
    pass

@extend_schema(
    tags=['User Authentication'],
    summary=_('Password reset request'),
    responses={
        200: OpenApiResponse(
            response=PasswordResetResponse,
            description=_('Submit password reset form'),
            examples=[
                OpenApiExample(
                    name=_('Password reset form submitted successfully'),
                    value=dict(status='OK'),
                    response_only=True
                )
            ]
        )
    }
)
class CustomResetPasswordRequestToken(ResetPasswordRequestToken):
    pass

@extend_schema(tags=['User Followings'])
class UserFollowingsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        artists = request.user.following.all()
        page = create_paginator(
            queryset=artists, 
            request=request, 
            view=self
        )
        serializer = UserFollowingsRetrieveSerializer(
            instance=page, 
            many=True
        )
        return Response(
            serializer.data, 
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        serializer = UserFollowingsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            artist = Artist.objects.get(pk=serializer.validated_data.get('artist_id'))
        except Artist.DoesNotExist:
            return Response(
                dict(
                    detail=_('Artist not found'),
                    code='not_found'
                ), status=status.HTTP_404_NOT_FOUND
            )
        
        ArtistFollow.objects.get_or_create(
            user=request.user,
            artist=artist
        )
        return Response(status=status.HTTP_200_OK)

@extend_schema(tags=['User Followings'])
class UserFollowingByIDView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, artist_id):
        artist_id = check_id_format(artist_id)
        if not artist_id:
            return Response(
                dict(
                    detail=_('The ID format is incorrect'), 
                    code='invalid_id_format'
                ), status=status.HTTP_400_BAD_REQUEST
            )        
        try:
            artist = Artist.objects.get(pk=artist_id)
            ArtistFollow.objects.get(
                user=request.user,
                artist=artist
            ).delete()

        except (Artist.DoesNotExist, ArtistFollow.DoesNotExist):
            return Response(
                dict(
                    detail=_('Artist not found'),
                    code='not_found'
                ), status=status.HTTP_404_NOT_FOUND
            )
        return Response(status=status.HTTP_200_OK)

@extend_schema(tags=['User Playlists'])
class UserPlaylistsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # throttle_classes = (UserRateThrottle,) # TODO
    
    def get(self, request):
        playlists = request.user.owned_playlists.all()
        if not playlists.exists():
            playlists.user.collaborative_playlists.all()

        page = create_paginator(
            queryset=playlists, 
            request=request, 
            view=self
        )
        serializer = UserPlaylistsRetrieveSerializer(
            instance=page,
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        serializer = UserPlaylistCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        playlist = Playlist.objects.create(name=serializer.validated_data.get('name'))
        request.user.playlists.add(playlist)
        return Response(status=status.HTTP_201_CREATED)
    
@extend_schema(tags=['User Playlists'])
class UserPlaylistByIDView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, playlist_id):
        try:
            playlist_id = uuid.UUID(playlist_id)
        except:
            return Response(
                dict(
                    detail=_('The ID format is incorrect'), 
                    code='invalid_id_format'
                ), status=status.HTTP_400_BAD_REQUEST
            )        
        queryset = Playlist.objects.filter(pk=playlist_id)
        page = create_paginator(
            queryset=queryset, 
            request=request, 
            view=self
        )
        serializer = UserPlaylistByIDRetrieveSerializer(
            instance=page,
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, playlist_id):
        try:
            playlist_id = uuid.UUID(playlist_id)
        except:
            return Response(
                dict(
                    detail=_('The ID format is incorrect'), 
                    code='invalid_id_format'
                ), status=status.HTTP_400_BAD_REQUEST
            )        
        try:
            Playlist.objects.get(pk=playlist_id).delete()
        except Playlist.DoesNotExist:
            return Response(
                dict(
                    detail=_('Playlist not found'),
                    code='not_found'
                ), status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, playlist_id):
        try:
            playlist_id = uuid.UUID(playlist_id)
        except:
            return Response(
                dict(
                    detail=_('The ID format is incorrect'), 
                    code='invalid_id_format'
                ), status=status.HTTP_400_BAD_REQUEST
            )        
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        serializer = UserPlaylistByIDUpdateSerializer(playlist, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data)
    
    def patch(self, request, playlist_id):
        try:
            playlist_id = uuid.UUID(playlist_id)
        except:
            return Response(
                dict(
                    detail=_('The ID format is incorrect'), 
                    code='invalid_id_format'
                ), status=status.HTTP_400_BAD_REQUEST
            )
        
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        serializer = UserPlaylistByIDUpdateSerializer(playlist, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data)
    
@extend_schema(tags=['User Playlists'])
class UserPlaylistTrackByIDView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @transaction.atomic
    def delete(self, request, playlist_id, track_id):
        try:
            Playlist.objects.filter(
                pk=playlist_id,
                tracks__pk=track_id
            ).delete()
        except:
            return Response(
                dict(
                    detail=_('Error removing track in playlist'), 
                    code='removing_failed'
                ), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
        
@extend_schema(tags=['User Liked Songs'])
class UserLikedSongsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        pass