from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenBlacklistView
)

from apps.v1.account import views


authentications_urls = [
    path('login/', TokenObtainPairView.as_view(), name='login-account'),
    path('token-refresh/', views.CustomTokenRefreshView.as_view(), name='token-refresh-account'),
    path('token-blacklist/', TokenBlacklistView.as_view(), name='token-blacklist-account'),
    path('register/', views.RegisterView.as_view(), name='register-account'),
    path('profile/', views.ProfileView.as_view(), name='profile-account'),
]

urlpatterns = [] + authentications_urls