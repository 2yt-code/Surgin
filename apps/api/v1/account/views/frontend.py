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
from rest_framework import (
    status,
    generics,
    permissions,
    views
)

from apps.api.v1.account.models import Device
from apps.api.v1.account.signals import set_access_token, set_auth_cookies
from apps.api.v1.account.swagger import (
    SuccessResponseSerializer,
    ErrorResponseSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer
)
from apps.api.v1.account.serializers import (
    RegisterSerializer,
    ProfileSerializer,
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer
)


User = get_user_model()

@extend_schema(
    tags=["Authentication"],
    summary=_('Login account'),
    description=_('Authenticates the user and validates their device and fingerprint before issuing access and refresh tokens'),
    request=CustomTokenObtainPairSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenObtainPairResponseSerializer,
            description=_('Login successful'),
            examples=[
                OpenApiExample(
                    name=_('Successful login account'),
                    value=dict(
                        access='access_token',
                        refresh='refresh_token'
                    ),
                    response_only=True
                )
            ]
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer, 
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
                    name=_('Failed login account'),
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

        device_model = Device.objects.get(uuid=serializer.validated_data.get('uuid'))
        set_auth_cookies(
            response, 
            serializer.validated_data.get('access'),
            serializer.validated_data.get('refresh'),
            device_model
        )
        return response

@extend_schema(
    tags=['Authentication'],
    summary=_('Refresh access token'),
    description=_('Refreshes an expired access token using a valid refresh token'),
    request=CustomTokenRefreshSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenRefreshResponseSerializer,
            description=_('Refresh token successful'),
            examples=[
                OpenApiExample(
                    name=_('Successful refresh token'),
                    value=dict(
                        access=_('access_token'),
                    ),
                    response_only=True
                )
            ]
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer,
            description=_('Refresh token faild'),
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
    tags=['Authentication'],
    summary=_('Register account'),
    description=_('Creates a new user account using the provided registration information'),
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            response=SuccessResponseSerializer,
            description=_('Register successful'),
            examples=[
                OpenApiExample(
                    name=_('Successful register account'),
                    value=dict(
                        detail=_('Register successful'),
                        code='registration_successful'
                    ),
                    response_only=True
                )
            ]
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description=_('Register faild'),
            examples=[
                OpenApiExample(
                    name=_('Failed register account'),
                    value=dict(
                        detail=_('Register failed'),
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
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except:
            return Response(
                dict(
                    detail=_('Register failed'),
                    code='registration_failed'
                ), status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            dict(
                detail=_('Register successful'),
                code='registration_successful'
            ), status=status.HTTP_201_CREATED
        )
 
# TODO
class ProfileView(views.APIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)