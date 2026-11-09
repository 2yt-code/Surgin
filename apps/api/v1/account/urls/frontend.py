from django.urls import path

from apps.api.v1.account import api_views


app_name = 'account'

authentication_urls = [
    path(
        'auth/login/', 
        api_views.CustomTokenObtainPairView.as_view(), 
        name='login-account'
    ),
    path(
        'auth/token-refresh/', 
        api_views.CustomTokenRefreshView.as_view(), 
        name='token-refresh-account'
    ),
    path(
        'auth/register/', 
        api_views.RegisterView.as_view(), 
        name='register-account'
    ),
    path(
        'auth/logout/', 
        api_views.LogoutView.as_view(), 
        name='logout-account'
    ),
    path(
        'auth/change-password/',
        api_views.ChangePasswordView.as_view(),
        name='change-password'
    ),
    path(
        'auth/password-reset/', 
        api_views.CustomResetPasswordRequestToken.as_view(), 
        name='reset-password-validate'
    ),
    path(
        'auth/password-reset/confirm/', 
        api_views.CustomResetPasswordConfirm.as_view(), 
        name='reset-password-confirm'
    ),
    path(
        'auth/password-reset/validate-token/', 
        api_views.CustomResetPasswordValidateToken.as_view(), 
        name='reset-password-validate'
    )
]
user_urls = [
    path(
        'user/',
        api_views.UserView.as_view(),
        name='user-account'
    ),
    path(
        'user/following/',
        api_views.UserFollowingsView.as_view(),
        name='user-followings-account'
    ),
    path(
        'user/following/<str:artist_id>/',
        api_views.UserFollowingByIDView.as_view(),
        name='user-followings-by-id-account'
    ),
    path(
        'user/playlist/',
        api_views.UserPlaylistsView.as_view(),
        name='user-playlists-account'
    ),
    path(
        'user/playlist/<str:playlist_id>/',
        api_views.UserPlaylistByIDView.as_view(),
        name='user-playlist-by-id-account'
    ),
    path(
        'user/playlist/<str:playlist_id>/track/<str:track_id>/',
        api_views.UserPlaylistTrackByIDView.as_view(),
        name='user-playlist-by-id-account'
    ),
    path(
        'user/liked-song/',
        api_views.UserLikedSongsView.as_view(),
        name='user-liked-songs-account'
    )
]

urlpatterns = [] + authentication_urls + user_urls