from datetime import timedelta

from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import exceptions


class ExploreFilter(filters.FilterSet):
    pass

class ExploreSearchFilter(filters.FilterSet):
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
        field_name='release_date',
        lookup_expr='year'
    )
    month = filters.NumberFilter(
        field_name='release_date',
        lookup_expr='month'
    )
    day = filters.NumberFilter(
        field_name='release_date',
        lookup_expr='day'
    )
    min_likes = filters.NumberFilter(
        field_name='like_count',
        lookup_expr='gte'
    )
    max_likes = filters.NumberFilter(
        field_name='like_count',
        lookup_expr='lte'
    )
    min_duration = filters.DurationFilter(
        field_name='duration',
        lookup_expr='gte'
    )
    max_duration = filters.DurationFilter(
        field_name='duration',
        lookup_expr='lte'
    )
    released = filters.CharFilter(method='filter_released')
    sort = filters.CharFilter(method='filter_sort')

    def filter_released(self, queryset, name, value):
        now = timezone.now()

        if value == 'today':
            start = now.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )
            end = start + timedelta(days=1)

        elif value == 'this_week':
            start = now.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            ) - timedelta(days=now.weekday())
            end = start + timedelta(days=7)

        elif value == 'this_month':
            start = now.replace(
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )

            if start.month == 12:
                end = start.replace(
                    year=start.year + 1,
                    month=1
                )
            else:
                end = start.replace(
                    month=start.month + 1
                )

        elif value == 'this_year':
            start = now.replace(
                month=1,
                day=1,
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )
            end = start.replace(
                year=start.year + 1
            )

        else:
            raise exceptions.ValidationError(
                'Invalid released value'
            )

        return queryset.filter(
            release_date__gte=start,
            release_date__lt=end
        )

    def filter_sort(self, queryset, name, value):
        sort_options = {
            'popular': '-like_count',
            'most_liked': '-like_count',
            'most_played': '-play_count',
            'latest': '-release_date',
            'oldest': 'release_date',
        }
        ordering = sort_options.get(value)

        if ordering is None:
            raise exceptions.ValidationError(
                'Invalid sort value'
            )

        return queryset.order_by(ordering)