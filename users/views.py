from rest_framework.views import APIView  # APIView 기반으로 REST API 만들기
from rest_framework.response import Response  # JSON 응답을 반환하기 위해 필요
from rest_framework.permissions import IsAuthenticated  # 로그인한 사용자만 접근 가능하도록 설정
from rest_framework_simplejwt.tokens import RefreshToken  # JWT 토큰 관련 기능 가져오기
from rest_framework import generics, permissions  # Django REST Framework의 Generic API View 사용
from django.contrib.auth.models import User  # User 모델 가져오기

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자(로그인한 사람)만 이 API 사용 가능

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
