"""
URL configuration for Diary_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from collections import UserList

from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from users.views import DeleteUserView, LoginView, LogoutView, ProfileView, SignUpView, VerifyEmailView, UserListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("login/", LoginView.as_view(), name="login"), # 로그인
    path("logout/", LogoutView.as_view(), name="logout"),  # 로그아웃 뷰
    path("profile/<str:nickname>/", ProfileView.as_view(), name="profile_name"),  # 프로필 조회/수정 뷰
    path("profile/<str:nickname>/delete/", DeleteUserView.as_view(), name="delete-user"),  # 유저 삭제 뷰

    path ("signup/", SignUpView.as_view(), name="signup"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify_email"),  # 이메일 인증 API
    path("email-verification-sent/", lambda request: render (request, "email_send.html"), name="email_sent"),
    path("users/", UserListView.as_view(), name="user_list"),
]