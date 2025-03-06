from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from rest_framework import (  # Django REST Framework의 Generic API View 사용
    generics, permissions, status, serializers)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken  # JWT 토큰 관련 기능 가져오기

from users.email_utils import send_verification_email
from users.forms import SignUpForm
from users.models import User
from users.serializers import UserSerializer


# 회원가입
class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "users/user_form.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.is_active = False  # 이메일 인증 전까지 비활성화
        user.save()

        # 이메일 인증 요청
        send_verification_email(user)
        return redirect("email_verification_sent")


class VerifyEmailView(APIView):
    def get(self, request):
        email = request.GET.get("email")
        token = request.GET.get("token")
        user = get_object_or_404(User, email=email)

        if default_token_generator.check_token(user, token):
            user.is_active = True  # ✅ 이메일 인증 후 계정 활성화
            user.save()
            return Response({"message": "이메일 인증이 완료되었습니다."}, status=200)
        return Response({"message": "유효하지 않은 토큰입니다."}, status=400)


# 로그인
class LoginView(generics.GenericAPIView):
    serializer_class = serializers.Serializer

    def post(self, request):
        # 클라이언트에서 보내온 사용자 이름과 비밀번호 추출
        email = request.data.get("email")
        password = request.data.get("password")

        # email, password를 활용해 사용자인증
        user = authenticate(email=email, password=password)
        if user is not None:
            # 사용자 인증 성공시 리프레시,엑세스토큰발급
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response(
                {"refresh_token": str(refresh), "access_token": str(access)},
                status=status.HTTP_200_OK,
            )
        # 인증 실패, 에러
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

# 로그인 폼을 제공하는 템플릿 뷰 (GET 요청 처리)
class LoginTemplateView(TemplateView):
    template_name = "users/login.html"


class LogoutView(generics.GenericAPIView):
    permission_classes = [
        IsAuthenticated
    ]  # 인증된 사용자(로그인한 사람)만 이 API 사용 가능

    def post(self, request):
        logout(request)

        # 클라이언트에서 "refresh" 키로 Refresh Token을 전달해야 함
        refresh_token = request.data.get("refresh")
        # 만약 refresh_token이 전달되지 않았다면 에러 반환
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # 토큰을 블랙리스트에 등록 (이제 이 토큰은 사용할 수 없음)
            except Exception as e:
                return Response({"error": f"토큰 등록 실패:  {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return redirect("login")




class ProfileView(generics.RetrieveUpdateAPIView):

    queryset = User.objects.all()  # User 모델을 대상으로 데이터 가져옴
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 접근 가능
    lookup_field = "nickname"

    def get_object(self):
        return self.request.user


class DeleteUserView(generics.DestroyAPIView):

    queryset = User.objects.all()  # User 모델을 대상으로 데이터 가져옴
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 접근 가능
    lookup_field = "nickname"

    def get_object(self):
        nickname = self.kwargs.get("nickname")  # nickname 가져오기

        if nickname:
            user = User.objects.get(nickname=nickname)
            if not user:  # 없을시 에러
                raise Response(
                    {"error": "해당 닉네임을 가진 사용자가 없습니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return user
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()

        return Response(
            {"message": f"'{user.nickname}' : Deleted successfully."}, status=200
        )


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

