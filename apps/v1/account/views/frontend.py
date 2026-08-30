from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from device_tracker.views import DeviceLogoutView
from device_tracker.models import Device
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import (
    status,
    generics,
    permissions,
)
from apps.v1.account.models import FingerPrint
from apps.v1.account.serializers import (
    RegisterSerializer,
    ProfileSerializer,
)
import utils


User = get_user_model()

class CustomTokenRefreshView(TokenRefreshView):
    throttle_classes = (UserRateThrottle,)

class CustomDeviceLogoutView(DeviceLogoutView):
    def get(self, request):
        key = utils.fingerprint.scheme_key(request)

        get_fingerprint_model = FingerPrint.objects.filter(key=key).first()
        if get_fingerprint_model:
            device = get_object_or_404(Device, pk=get_fingerprint_model.pk, user=request.user)
        else: pass # TODO Resolving the "not found in database" issue

        if device.refresh_token_jti:
            try:
                token = OutstandingToken.objects.get(jti=device.refresh_token_jti)
                BlacklistedToken.objects.get_or_create(token=token)
            except OutstandingToken.DoesNotExist:
                pass

        get_fingerprint_model.delete()
        device.delete()

        return Response(
            {'detail': 'device logged out'},
            status=status.HTTP_200_OK
        )

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'status': _('success')}, 
            status=status.HTTP_201_CREATED
            )
 
class ProfileView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)