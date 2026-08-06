from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
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


User = get_user_model()    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'status': _('success')}, 
                status=status.HTTP_201_CREATED
                )

        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )
 
class ProfileView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ProfileSerializer