from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise serializers.ValidationError('Invalid credentials')
            else:
                attrs['user'] = user
                return attrs
        else:
            raise serializers.ValidationError('Both username and password in required')

class RegisterSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).first():
            raise serializers.ValidationError({'email': 'Email already exists'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            username=validated_data.get('username'),
            email=validated_data.get('email'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username', 
            'email', 
            'password',
            ]
        
        extra_kwrags = {
            'password': {'write_only': True}
        }