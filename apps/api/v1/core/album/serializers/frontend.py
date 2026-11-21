from rest_framework import serializers


class AlbumBasicInformationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()