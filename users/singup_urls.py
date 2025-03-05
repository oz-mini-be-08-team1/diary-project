from django.shortcuts import render
from django.urls import path

from users.signup_views import SignUpView, VerityEmailView

urlpatterns = [
    path ("signup/", SignUpView.as_view(), name="signup"),
    path("verify-email/", VerityEmailView.as_view(), name="verify_email"),  # ✅ 이메일 인증 API
    path("email-verification-sent/", lambda request: render(request, "users/email_verification_sent.html"),
         name="email_verification_sent"),
]