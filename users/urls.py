from django.shortcuts import render
from django.urls import path

from users.views import (DeleteUserView, LoginView, LogoutView, ProfileView,
                         SignUpView, UserListView, VerifyEmailView, LoginTemplateView)
urlpatterns = [
    path("login/", LoginTemplateView.as_view(), name="login_page"),  # 로그인
    path("login-api/", LoginView.as_view(), name="login_api"),  # 🔥 로그인 API (POST 요청)

    path("logout/", LogoutView.as_view(), name="logout"),  # 로그아웃 뷰
    path("profile/<str:nickname>/", ProfileView.as_view(), name="profile_name"),  # 프로필 조회/수정 뷰
    path("profile/<str:nickname>/delete/", DeleteUserView.as_view(), name="delete_user"),  # 유저 삭제 뷰
    path("signup/", SignUpView.as_view(), name="signup"),
    path("userlist/", UserListView.as_view(), name="user_list"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify_email"),  # 이메일 인증 API
    path("email-verification-sent/", lambda request: render(request, "email_send.html"), name="email_sent"),

]