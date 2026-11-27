from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
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

from apps.api.v1.account.swaggers import (
    SchemaResponseSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    UserResponseSerializer,
    PasswordResetResponse,
    PasswordResetErrorResponse
)
from apps.api.v1.account.selectors import (
    get_device, 
    get_user_all
)
from apps.api.v1.account.services import (
    clear_auth_cookie, 
    create_user_following, 
    create_user_playlist, 
    delete_user_following, 
    delete_user_playlist_by_id, 
    delete_user_playlist_track_by_id, 
    get_user_following, 
    get_user_playlist, 
    get_user_playlist_by_id,
    send_restore_account_email, 
    set_access_token, 
    set_auth_cookies, 
    update_user_playlist_by_id,
    user_activation_account,
    user_add_track_playlist,
    user_change_password,
    user_logout,
    user_restore_account
)
from apps.api.v1.account.serializers import (
    RegisterSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
    UserActivationAccountSerializer,
    UserSendEmailRestoreAccountSerializer,
    UserRestoreAccountSerializer
)


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

        device_model = get_device(pk=serializer.validated_data.get('device_id'))
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
class UserRegisterView(generics.CreateAPIView):
    queryset = get_user_all()
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

@extend_schema(tags=['User Authentication'])
class UserActivationAccount(views.APIView):
    def post(self, request):
        serializer = UserActivationAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_activation_account(
            uidb64=serializer.validated_data.get('uid'),
            token=serializer.validated_data.get('token'),
        )
        return Response(status=status.HTTP_200_OK)
    
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
    queryset = get_user_all()
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
class UserLogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        is_valid_logout = user_logout(request)
        if not is_valid_logout:
            return Response(
                dict(
                    detail=_('Logout unsuccessful'),
                    code='logout_unsuccessful'
                ), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = Response(status=status.HTTP_204_NO_CONTENT)
        clear_auth_cookie(response=response)
        return response

@extend_schema(tags=['User Authentication'])
class UserChangePasswordView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def patch(self, request):
        user_change_password(request)
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

@extend_schema(tags=['User Authentication'])
class UserSendEmailRestoreAccount(views.APIView):    
    def post(self, request):
        serializer = UserSendEmailRestoreAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_restore_account_email(email=serializer.validated_data.get('email'))
        return Response(status=status.HTTP_200_OK)
    
@extend_schema(tags=['User Authentication'])
class UserRestoreAccount(views.APIView):
    def post(self, request):
        serializer = UserRestoreAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_restore_account(
            uidb64=serializer.validated_data.get('uid'),
            token=serializer.validated_data.get('token')
        )
        return Response(status=status.HTTP_200_OK)

@extend_schema(tags=['User Followings'])
class UserFollowingView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        data = get_user_following(request)
        return Response(data)
    
    def post(self, request):
        create_user_following(request)
        return Response(status=status.HTTP_200_OK)

@extend_schema(tags=['User Followings'])
class UserFollowingByIDView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, artist_id):
        delete_user_following(request, artist_id)
        return Response(status=status.HTTP_200_OK)

@extend_schema(tags=['User Playlists'])
class UserPlaylistView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        data = get_user_playlist(request)
        return Response(data)
    
    def post(self, request):
        create_user_playlist(request)
        return Response(status=status.HTTP_201_CREATED)
    
@extend_schema(tags=['User Playlists'])
class UserPlaylistByIDView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, playlist_id):
        data = get_user_playlist_by_id(playlist_id)
        return Response(data)
    
    def delete(self, request, playlist_id):
        delete_user_playlist_by_id(playlist_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, playlist_id):
        data = update_user_playlist_by_id(request, playlist_id)
        return Response(data)
    
    def patch(self, request, playlist_id):
        data = update_user_playlist_by_id(request, playlist_id)
        return Response(data)
    
@extend_schema(tags=['User Playlists'])
class UserPlaylistTrackByIDView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, playlist_id, track_id):
        delete_user_playlist_track_by_id(playlist_id, track_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@extend_schema(tags=['User Playlists'])
class UserPlaylistTrackView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, playlist_id):
        user_add_track_playlist(request, playlist_id)
        return Response(status=status.HTTP_200_OK)
        
@extend_schema(tags=['User Liked Songs'])
class UserLikedSongsView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        pass