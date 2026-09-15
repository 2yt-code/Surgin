from django.urls import path

from apps.api.v1.core import views

explore_urls = [
    path('explore/'),
    path('explore/search/'),
]

urlpatterns = [] + explore_urls