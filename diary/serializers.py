from rest_framework import serializers
from .models import Diary

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['diary_id', 'title', 'tag', 'detail', 'created_at', 'updated_at', 'mood']
