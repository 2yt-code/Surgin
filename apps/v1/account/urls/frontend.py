from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.v1.account import views


authentications_urls = [
    path('token', TokenObtainPairView.as_view(), name='login-account'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register-account'),
    path('profile/', views.ProfileView.as_view(), name='profile-account'),
]

urlpatterns = [] + authentications_urls