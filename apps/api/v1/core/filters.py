from django_filters import rest_framework as filters


class ExploreFilter(filters.FilterSet):
    title = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains'
    )
    # artist = filters.CharFilter(
    #     field_name='artist__name',
    #     lookup_expr='icontains'
    # )
    # album = filters.CharFilter(
    #     field_name='album__name',
    #     lookup_expr='icontains'
    # ) # TODO
    genre = filters.CharFilter(
        field_name='genre',
        lookup_expr='icontains'
    )
    year = filters.NumberFilter(
        field_name="release_date",
        lookup_expr="year"
    )
    month = filters.NumberFilter(
        field_name="release_date",
        lookup_expr="month"
    )
    day = filters.NumberFilter(
        field_name="release_date",
        lookup_expr="day"
    )
    min_likes = filters.NumberFilter(
        field_name="like_count",
        lookup_expr="gte"
    )
    max_likes = filters.NumberFilter(
        field_name="like_count",
        lookup_expr="lte"
    )
    min_duration = filters.DurationFilter(
        field_name="duration",
        lookup_expr="gte"
    )
    max_duration = filters.DurationFilter(
        field_name="duration",
        lookup_expr="lte"
    )