from rest_framework import serializers

class ArtistSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    bio = serializers.CharField()
    avatar = serializers.ImageField()
    cover = serializers.ImageField()
    popularity = serializers.IntegerField()
    verified = serializers.BooleanField()
    artist_type = serializers.CharField()

class ArtistBasicInformationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    avatar = serializers.ImageField()