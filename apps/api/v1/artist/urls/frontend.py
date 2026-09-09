from django.urls import path
from apps.api.v1.artist import views


urlpatterns = [
    path('register/', views.RegisterArtistAccountView.as_view(), name='register-artist')
]
