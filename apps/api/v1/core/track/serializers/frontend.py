from rest_framework import serializers

from apps.api.v1.core.track.models import Track

class TrackSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=200,
        required=True
    )
    cover = serializers.ImageField(required=True)
    audio_file = serializers.FileField(required=True)
    genre = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    duration = serializers.DurationField(required=True)

class TrackByIDSerializer(serializers.ModelSerializer):
    album = serializers.StringRelatedField(many=True)
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Track
        fields = [
            'title',
            'cover',
            'audio_file',
            'album',
            'genres',
            'description',
            'duration',
            'play_count',
            'created'
        ]
        
class ExploreSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['uuid']