from rest_framework import generics
from django_filters import rest_framework as filters

from apps.api.v1.core.song.filters import ExploreFilter
from apps.api.v1.core.song.models import Song
from apps.api.v1.core.song.serializers import SongSerializer


class ExploreView(generics.ListAPIView):
    pass

class ExploreSearchView(generics.ListAPIView):
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExploreFilter