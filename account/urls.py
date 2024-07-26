# accounts/urls.py
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # 회원가입/로그인/로그아웃
    path("join/", RegisterView.as_view()), # 회원가입
    path("login/", AuthView.as_view()), # 로그인
    path("logout/", LogoutView.as_view()), # 로그아웃
]