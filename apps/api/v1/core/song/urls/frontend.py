from django.urls import path

from apps.api.v1.core.song import views

explore_urls = [
    # path('explore/'),
    path(
        'explore/search', 
        views.ExploreSearchView.as_view(), 
        name='explore-search'
    ),
]

urlpatterns = [] + explore_urls