from itertools import count
from rest_framework import serializers

from apps.v1.artist.models import Artist


class RegisterArtistAccountSerializers(serializers.ModelSerializer):
    # confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Artist
        fields = [
            'name',
            'first_name',
            'last_name',
            'email',
            'gender',
            'dob',
            'country',
            'avatar',
            'baner',
            # 'password',
            # 'confirm_password'
        ]
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def validate(self, attrs):
        if Artist.objects.filter(name=attrs.get('name')).first():
            return serializers.ValidationError({'name': 'Name already exists'})
        
        if Artist.objects.filter(first_name=attrs.get('first_name')).first():
            return serializers.ValidationError({'first_name': 'FirstName already exists'})
        
        if Artist.objects.filter(last_name=attrs.get('last_name')).first():
            return serializers.ValidationError({'last_name': 'LastName already exists'})
        
        if Artist.objects.filter(email=attrs.get('email')).first():
            return serializers.ValidationError({'email': 'Email already exists'})
        return attrs
        
        # if attrs.get('password') != attrs.get('confirm_password'):
        #     return serializers.ValidationError({'password': 'Password fields didnt match'})
        
    def create(self, validated_data):
        artist = Artist.objects.create(
            name=validated_data.get('name'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            gender=validated_data.get('gender'),
            dob=validated_data.get('dob'),
            country=validated_data.get('country'),
            avatar=validated_data.get('avatar'),
            baner=validated_data.get('baner')
        )
        # user.set_password(validated_data.get('password'))
        artist.save()
        return artist