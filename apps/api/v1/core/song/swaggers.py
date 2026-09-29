from rest_framework import serializers


class SongResponseSerailizer(serializers.Serializer):
    title = serializers.CharField()
    # artist = serializers.PrimaryKeyRelatedField()
    # album = serializers.PrimaryKeyRelatedField()
    cover = serializers.ImageField()
    audio_file = serializers.FileField()
    genre = serializers.CharField()
    release_date = serializers.DateTimeField()
    description = serializers.CharField()
    duration = serializers.DurationField()
    play_count = serializers.IntegerField()
    like_count = serializers.IntegerField()
    updated_at = serializers.DateTimeField()

class SongNotFoundResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()

class ExploreSearchResponseSerializer(serializers.Serializer):
    uuid = serializers.CharField()