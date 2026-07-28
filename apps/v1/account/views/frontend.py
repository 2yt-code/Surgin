from django.contrib.auth import get_user_model
from django.contrib.auth import login
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from apps.v1.account.serializers import (
    RegisterSerializer,
    LoginSerializer
)


User = get_user_model()

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)

            return Response(
                {'token': token.key},
                status=status.HTTP_200_OK
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )
            
    
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