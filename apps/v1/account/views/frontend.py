from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from apps.v1.account.serializers import RegisterSerializer


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'success'}, 
                status=status.HTTP_201_CREATED
                )

        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )