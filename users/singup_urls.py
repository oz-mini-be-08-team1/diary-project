from django.shortcuts import render
from django.urls import path

from users.views import SignUpView, VerifyEmailView

urlpatterns = [
    path ("signup/", SignUpView.as_view(), name="signup"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify_email"),  # 이메일 인증 API
    path("email-verification-sent/", lambda request: render (request, "email_send.html"), name="email_sent"),
]