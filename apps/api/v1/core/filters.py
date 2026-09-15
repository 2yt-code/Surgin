from django_filters import rest_framework as filters

from apps.api.v1.core.models import Song


class ExploreFilter(filters.FilterSet):
    created_as = filters.CharFilter(
        field_name='genre',
    )

    class Meta:
        model = Song