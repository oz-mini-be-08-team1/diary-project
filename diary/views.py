from django.db.models import Q
from django.utils.dateparse import parse_date
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Diary
from .serializers import DiarySerializer


# Create your views here.
# 일기 작성
class DiaryCreateView(generics.CreateAPIView):
    queryset = Diary.objects.all() #모든 일기 데이터 호출
    serializer_class = DiarySerializer # serializer사용하여 직렬화
    permission_classes = [IsAuthenticated] #로그인한 사용자만 혀용

    def perform_create(self, serializer):
        #일기 작성 시 로그인한 사용자정보 추가
        serializer.save(author=self.request.user)# 일기 쓴사람 author로 정의

class DiaryUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        diary = super().get_object()
        if diary.author != self.request.user:
            raise PermissionDenied("본인 일기만 수정 가능")
        return diary

class DiaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

class DiaryDeleteView(generics.DestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        diary = super().get_object()
        if diary.author != self.request.user:
            raise PermissionDenied("본인 일기만 삭제 가능")
        return diary

class DiaryListView(generics.ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Diary.objects.filter(author=self.request.user) # 특정 사용자의 리스트
        q = self.request.GET.get('q') # 제목,내용에서 검색
        date = self.request.GET.get('date',"") # 날짜로 검색
        sort = self.request.GET.get("sort", "new")  # 정렬 기준 (기본값: 최신순)

        if q:
            queryset = queryset.filter(   # 검색
                Q(title__icontains=q) |
                Q(detail__icontains=q)
                )
        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                queryset = queryset.filter(created_at__date=parsed_date)

        if sort == "old":
            queryset = queryset.order_by("created_at")  # 오래된 순
        else:
            queryset = queryset.order_by("-created_at")  # 최신순 (기본값)

        return queryset


class HomeView(TemplateView):
    template_name = "home.html"

