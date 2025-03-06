from django.contrib.auth import authenticate
from django.contrib.auth.models import User  # User 모델 가져오기
from rest_framework import generics,permissions,status # Django REST Framework의 Generic API View 사용
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken  # JWT 토큰 관련 기능 가져오기
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.email_utils import send_verification_email
from users.models import User

# 회원가입
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


class VerifyEmailView(APIView):
   def get(self, request):
       email = request.GET.get('email')
       token = request.GET.get('token')
       user = get_object_or_404(User, email=email)

       if default_token_generator.check_token(user, token):
           user.is_active = True  # ✅ 이메일 인증 후 계정 활성화
           user.save()
           return Response({"message": "이메일 인증이 완료되었습니다."}, status=200)
       return Response({"message": "유효하지 않은 토큰입니다."}, status=400)

# 로그인
class LoginView(generics.GenericAPIView):
    def post(self, request):
        # 클라이언트에서 보내온 사용자 이름과 비밀번호 추출
        username = request.data.get('username')
        password = request.data.get('password')

        #username과 password를 활용해 사용자인증
        user = authenticate(username=username, password=password)
        if user is not None:
            #사용자 인증 성공시 리프레시,엑세스토큰발급
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response({
                "refresh_token": str(refresh),
                "access_token": str(access)
            }, status = status.HTTP_200_OK)
        #인증 실패, 에러
        return Response({"error": "Invalid credentials"}, status = status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):
    permission_classes = [
        IsAuthenticated
    ]  # 인증된 사용자(로그인한 사람)만 이 API 사용 가능

    def post(self, request):

        try:
            # 클라이언트에서 "refresh" 키로 Refresh Token을 전달해야 함
            refresh_token = request.data.get("refresh")

            # 만약 refresh_token이 전달되지 않았다면 에러 반환
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=400)

            # RefreshToken 객체 생성 후, 해당 토큰을 블랙리스트에 추가
            token = RefreshToken(refresh_token)
            token.blacklist()  # 토큰을 블랙리스트에 등록 (이제 이 토큰은 사용할 수 없음)

            return Response({"message": "Logged out successfully"}, status=200)

        except Exception as e:
            # 예외 발생 시 에러 메시지 반환
            return Response({"error": str(e)}, status=400)


class ProfileView(generics.RetrieveUpdateAPIView):

    queryset = User.objects.all()  # User 모델을 대상으로 데이터 가져옴
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def get_object(self):
        return self.request.user


class DeleteUserView(generics.DestroyAPIView):

    queryset = User.objects.all()  # User 모델을 대상으로 데이터 가져옴
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()  # 현재 로그인한 사용자 가져오기
        user.delete()  # 유저 삭제

        return Response({"message": "Deleted successfully"}, status=200)
