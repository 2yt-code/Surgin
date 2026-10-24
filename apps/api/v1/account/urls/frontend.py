from django.urls import path

from apps.api.v1.account import views

app_name = 'account'

authentication_urls = [
    path(
        'auth/login/', 
        views.CustomTokenObtainPairView.as_view(), 
        name='login-account'
    ),
    path(
        'auth/token-refresh/', 
        views.CustomTokenRefreshView.as_view(), 
        name='token-refresh-account'
    ),
    path(
        'auth/register/', 
        views.RegisterView.as_view(), 
        name='register-account'
    ),
    path(
        'auth/logout/', 
        views.LogoutView.as_view(), 
        name='logout-account'
    ),
    path(
        'auth/password-reset/', 
        views.CustomResetPasswordRequestToken.as_view(), 
        name='reset-password-validate'
    ),
    path(
        'auth/password-reset/confirm/', 
        views.CustomResetPasswordConfirm.as_view(), 
        name='reset-password-confirm'
    ),
    path(
        'auth/password-reset/validate-token/', 
        views.CustomResetPasswordValidateToken.as_view(), 
        name='reset-password-validate'
    ),
    path(
        'user/',
        views.UserView.as_view(),
        name='user-data-account'
    ),
    path(
        'user/followings/',
        views.UserFollowingsView.as_view(),
        name='user-data-account'
    ),
    path(
        'user/playlists/',
        views.UserPlaylistsView.as_view(),
        name='user-data-account'
    )
]

urlpatterns = [] + authentication_urls