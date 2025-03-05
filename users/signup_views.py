from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.email_utils import send_verification_email
from users.models import User


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False  # 이메일 인증 전까지 비활성화
        user.save()

        # 이메일 인증 요청
        send_verification_email(user)
        return redirect("email_verification_sent")


class VerityEmailView(APIView):
   def get(self, request):
       email = request.GET.get('email')
       token = request.GET.get('token')
       user = get_object_or_404(User, email=email)

       if default_token_generator.check_token(user, token):
           user.is_active = True  # ✅ 이메일 인증 후 계정 활성화
           user.save()
           return Response({"message": "이메일 인증이 완료되었습니다."}, status=200)
       return Response({"message": "유효하지 않은 토큰입니다."}, status=400)