from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import (
    TokenViewBase
)
from rest_framework import (
    status,
    generics,
    permissions,
)
from apps.api.v1.account.models import Device
from apps.api.v1.account.signals import set_access_token, set_auth_cookies
from apps.api.v1.account.serializers import (
    RegisterSerializer,
    ProfileSerializer,
)


User = get_user_model()

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

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(
                {'status': _('Faild')}
            )
        serializer.save()

        return Response(
            {'status': _('Success')}, 
            status=status.HTTP_201_CREATED
            )
 
class ProfileView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)