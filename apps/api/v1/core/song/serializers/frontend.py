from rest_framework import serializers

from apps.api.v1.core.song.models import Song

# TODO
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = [
            'id',
            'title',
            'cover',
            'audio_file',
            'genre',
            'release_date',
            'description',
            'duration',
            'play_count',
            'like_count',
            'updated_at'
        ]
        