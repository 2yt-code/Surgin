from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.throttling import UserRateThrottle
from rest_framework.response import Response
from rest_framework import (
    status,
    generics,
    permissions,
)
from apps.v1.account.serializers import (
    RegisterSerializer,
    ProfileSerializer
)
from apps.v1.account.models import FingerPrint


User = get_user_model()    

class CustomTokenRefreshView(TokenRefreshView):
    throttle_classes = UserRateThrottle

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(username=serializer.validated_data.get('username'))

        fingerprint = FingerPrint.objects.create(
            user_id=user.id,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
        )
        fingerprint.save()

        return Response(
            {'status': _('success')}, 
            status=status.HTTP_201_CREATED
            )
 
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user.id