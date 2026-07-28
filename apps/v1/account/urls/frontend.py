from django.urls import path

from apps.v1.account import views


authentications_urls = [
    path('login/', views.LoginView.as_view(), name='login-account'),
    # path('logout/', views.LogoutView.as_view(), name='logout-account')
    path('register/', views.RegisterView.as_view(), name='register-account'),
]

urlpatterns = [] + authentications_urls