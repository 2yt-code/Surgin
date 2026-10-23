from django.urls import path

from apps.api.v1.account import views

app_name = 'account'

authentication_urls = [
    path(
        'login/', 
        views.CustomTokenObtainPairView.as_view(), 
        name='login-account'
    ),
    path(
        'token-refresh/', 
        views.CustomTokenRefreshView.as_view(), 
        name='token-refresh-account'
    ),
    path(
        'register/', 
        views.RegisterView.as_view(), 
        name='register-account'
    ),
    path(
        'dashboard/', 
        views.DashboardView.as_view(), 
        name='profile-account'
    ),
    path(
        'logout/', 
        views.LogoutView.as_view(), 
        name='logout-account'
    ),
    path(
        'password-reset/', 
        views.CustomResetPasswordRequestToken.as_view(), 
        name='reset-password-validate'
    ),
    path(
        'password-reset/confirm/', 
        views.CustomResetPasswordConfirm.as_view(), 
        name='reset-password-confirm'
    ),
    path(
        'password-reset/validate-token/', 
        views.CustomResetPasswordValidateToken.as_view(), 
        name='reset-password-validate'
    ),
]

urlpatterns = [] + authentication_urls