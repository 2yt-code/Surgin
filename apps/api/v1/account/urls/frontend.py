from django.urls import path

from apps.api.v1.account import views


authentications_urls = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login-account'),
    path('token-refresh/', views.CustomTokenRefreshView.as_view(), name='token-refresh-account'),
    path('register/', views.RegisterView.as_view(), name='register-account'),
    path('profile/', views.ProfileView.as_view(), name='profile-account'),
]

urlpatterns = [] + authentications_urls