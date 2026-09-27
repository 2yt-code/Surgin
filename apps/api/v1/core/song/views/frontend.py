from rest_framework import generics, views
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
    OpenApiResponse,
    OpenApiExample
)

from apps.api.v1.core.song.models import Song
from apps.api.v1.core.song.paginations import ExploreSearchPagination
from apps.api.v1.core.song.swagger import (
    ExploreSearchResponseSerializer, 
    SongNotFoundResponseSerializer, 
    SongResponseSerailizer
)
from apps.api.v1.core.song.filters import (
    ExploreFilter, 
    ExploreSearchFilter
)
from apps.api.v1.core.song.serializers import (
    ExploreSearchSerializer,
    SongSerializer
)


# TODO
@extend_schema(tags=['Explore'])
class ExploreView(views.APIView):
    # serializer_class = ExploreSearchSerializer
    # queryset = Song.objects.all()
    # pagination_class = ExplorePagination
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = None
    pass
# TODO
@extend_schema(
    tags=['Explore'],
    summary=_('Search and explore songs'),
    description=_(
        'Search, filter, and sort songs by title, genre, release date, likes, duration, and popularity '
        'Multiple query parameters can be combined'
    ),
    responses={
        200: OpenApiResponse(
            response=ExploreSearchResponseSerializer,
            description=_(
                'Returns a list of songs matching the specified search '
                'and filter parameters'
            ),
            examples=[
                OpenApiExample(
                    name=_('Successful song search'),
                    value=[
                        dict(uuid='song_uuid')
                    ],
                    response_only=True,
                ),
                OpenApiExample(
                    name=_('No matching songs'),
                    value=[],
                    response_only=True,
                ),
            ],
        ),
    },
    parameters=[
        OpenApiParameter(
            name='title',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_(
                'Search for songs whose title contains the specified text'
            ),
        ),
        OpenApiParameter(
            name='genre',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_(
                'Filter songs by genre. Partial genre names are supported'
            ),
        ),
        OpenApiParameter(
            name='year',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_(
                'Filter songs by the year of their release date'
            ),
        ),
        OpenApiParameter(
            name='month',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_(
                'Filter songs by the month of their release date '
                'Expected value: 1-12'
            ),
        ),
        OpenApiParameter(
            name='day',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_(
                'Filter songs by the day of their release date '
                'Expected value: 1-31'
            ),
        ),
        OpenApiParameter(
            name='min_likes',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_(
                'Return songs with a like count greater than or equal '
                'to the specified value'
            ),
        ),
        OpenApiParameter(
            name='max_likes',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_(
                'Return songs with a like count less than or equal '
                'to the specified value'
            ),
        ),
        OpenApiParameter(
            name='min_duration',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_(
                'Return songs with a duration greater than or equal '
                'to the specified value. Format: HH:MM:SS'
            ),
        ),
        OpenApiParameter(
            name='max_duration',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_(
                'Return songs with a duration less than or equal '
                'to the specified value. Format: HH:MM:SS'
            ),
        ),
        OpenApiParameter(
            name='released',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            enum=[
                'today',
                'this_week',
                'this_month',
                'this_year',
            ],
            description=_(
                'Filter songs by release period '
                'Supported values: today, this_week, '
                'this_month, and this_year'
            ),
        ),
        OpenApiParameter(
            name='sort',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=False,
            enum=[
                'popular',
                'most_liked',
                'most_played',
                'latest',
                'oldest',
            ],
            description=_(
                'Sort the search results by popularity, like count, '
                'play count, release date, or title'
            ),
        ),
    ],
)
class ExploreSearchView(generics.ListAPIView):
    serializer_class = ExploreSearchSerializer
    queryset = Song.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ExploreSearchFilter
    pagination_class = ExploreSearchPagination

@extend_schema(
    tags=['Song'],
    summary=_('Get song details'),
    description=_(
        'Retrieve detailed information about a specific song '
        'using its UUID'
    ),
    parameters=[
        OpenApiParameter(
            name='uuid',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            required=True,
            description=_('Unique identifier of the song'),
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=SongResponseSerailizer,
            description=_('Song information retrieved successfully'),
            examples=[
                OpenApiExample(
                    name=_('Successful get song'),
                    value={
                        'uuid': 'song_uuid',
                        'title': 'song_title',
                        'artist': 'song_artist',
                        'album': 'song_album',
                        'cover': 'song_cover.png',
                        'audio_file': 'song_audio_file.mp3',
                        'release_date': 'song_release_date',
                        'genre': 'song_genre',
                        'description': 'song_description',
                        'play_count': 1000,
                        'like_count': 250,
                        'duration': 'song_duration',
                        'updated_at': 'song_updated_at',
                    },
                    response_only=True,
                ),
            ],
        ),
        404: OpenApiResponse(
            response=SongNotFoundResponseSerializer,
            description=_('Song not found'),
            examples=[
                OpenApiExample(
                    name=_('Song not found'),
                    value=dict(detail='No Song matches the given query'),
                    response_only=True,
                ),
            ],
        ),
    },
)
class SongView(generics.RetrieveAPIView):
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    lookup_field = 'uuid'