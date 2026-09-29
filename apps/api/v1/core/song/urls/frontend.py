from django.urls import path

from apps.api.v1.core.song import views


explore_urls = [
    path(
        'explore/', 
        views.ExploreView.as_view(), 
        name='explore'
    ),
    path(
        'explore/search/', 
        views.ExploreSearchView.as_view(), 
        name='explore-search'
    ),
    path(
        '<str:uuid>/',
        views.SongView.as_view(),
        name='song'
    )
]

urlpatterns = [] + explore_urls