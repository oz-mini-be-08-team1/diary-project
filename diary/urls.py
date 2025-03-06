
from django.urls import path

from diary.views import DiaryCreateView, DiaryListView, DiaryUpdateView, DiaryDeleteView, DiaryDetailView

urlpatterns = [
    path('create/', DiaryCreateView.as_view(), name='diary_create'),
    path('list/', DiaryListView.as_view(), name='diary_list'),
    path('<int:diary_id>/update/', DiaryUpdateView.as_view(), name='diary_update'),
    path('<int:diary_id>/detail/', DiaryDetailView.as_view(), name='diary_update'),

    path('<int:diary_id>/delete/', DiaryDeleteView.as_view(), name='diary_delete'),

]