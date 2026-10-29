from django.urls import path

from apps.api.v1.core.song import api_views

app_name = 'song'

explore_urls = [
    path(
        'explore/', 
        api_views.ExploreView.as_view(), 
        name='explore'
    ),
    path(
        'explore/search/', 
        api_views.ExploreSearchView.as_view(), 
        name='explore-search'
    ),
    path(
        '<str:uuid>/',
        api_views.SongView.as_view(),
        name='song'
    )
]

urlpatterns = [] + explore_urls