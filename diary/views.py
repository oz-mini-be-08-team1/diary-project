from django.db.models import Q
from django.utils.dateparse import parse_date
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

# 일기 조회
class DiarylistView(generics.ListAPIView):
    queryset = Diary.objects.all().order_by('-created_at') # 최신순으로 정렬
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Diary.objects.all().order_by('-created_at')

class DiaryUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        diary = super().get_object()
        if diary.author != self.request.user:
            raise PermissionDenied("본인 일기만 수정가능")
        return diary

class DiaryDeleteView(generics.DestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        diary = super().get_object()
        if diary.author != self.request.user:
            raise PermissionDenied("본인 일기만 삭제가능")
        return diary

class DiaryListView(generics.ListAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        queryset = Diary.objects.all()
        sort = self.request.GET.get('sort','new')
        q = self.request.GET.get('q')
        date = self.request.GET.get('date',"")

        if sort == 'old':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        if q:
            queryset = queryset.filter(   # 검색
                Q(title__icontains=q) |
                Q(detail__icontains=q)
                )
        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                queryset = queryset.filter(created_at__date=parsed_date)

        return queryset



