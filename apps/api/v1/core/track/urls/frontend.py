from django.urls import path

from apps.api.v1.core.track import api_views


app_name = 'track'

track_urls = [
    path(
        '',
        api_views.TrackView.as_view(),
        name='track'
    ),
    path(
        '<str:track_id>/',
        api_views.TrackByIDView.as_view(),
        name='track-by-id'
    )
]

urlpatterns = [] + track_urls