from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView
)

from apps.v1.account import views


authentications_urls = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login-account'),
    path('token-refresh/', views.CustomTokenRefreshView.as_view(), name='token-refresh-account'),
    path('token-blacklist/', TokenBlacklistView.as_view(), name='token-blacklist-account'),
    path('register/', views.RegisterView.as_view(), name='register-account'),
    path('profile/', views.ProfileView.as_view(), name='profile-account'),
    # path('logout/', views.CustomDeviceLogoutView.as_view(), name='logout-account')
]

urlpatterns = [] + authentications_urls