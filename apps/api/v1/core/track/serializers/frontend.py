from rest_framework import serializers

from apps.api.v1.account.selectors import get_album_by_filter_method, get_track_credit_by_filter_method
from apps.api.v1.core.album.serializers import AlbumBasicInformationSerializer
from apps.api.v1.core.track.models import Track

class TrackSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    cover = serializers.ImageField()
    audio_file = serializers.FileField()
    genre = serializers.CharField()
    description = serializers.CharField()
    duration = serializers.DurationField()

class TrackCreditBasicInformationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    artist = serializers.CharField()

class TrackBasicInformationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    cover = serializers.ImageField()
    duration = serializers.DurationField()
    album = serializers.SerializerMethodField()
    artist = serializers.SerializerMethodField()

    def get_artist(self, obj):
        track_credit = get_track_credit_by_filter_method(track=obj)
        if not track_credit:
            return None
        return TrackCreditBasicInformationSerializer(instance=track_credit, many=True).data
    
    def get_album(self, obj):
        albums = get_album_by_filter_method(tracks=obj)
        if not albums:
            return None
        return AlbumBasicInformationSerializer(instance=albums, many=True).data

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