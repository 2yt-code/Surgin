from rest_framework import serializers

from apps.api.v1.core.track.models import Track

class TrackSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=200,
        
    )
    cover = serializers.ImageField()
    audio_file = serializers.FileField()
    genre = serializers.CharField()
    description = serializers.CharField()
    duration = serializers.DurationField()

class TrackByIDSerializer(serializers.ModelSerializer):
    album = serializers.StringRelatedField(many=True)
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Track
        fields = [
            'id',
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