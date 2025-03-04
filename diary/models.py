import uuid
from django.db import models
from django.db.migrations.operations.models import ModelOperation


# Create your models here.
class Diary(models.Model):
    MOOD_CHOICES = [
        ('기쁨', '기쁨'),
        ('슬픔', '슬픔'),
        ('분노', '분노'),
        ('피곤', '피곤'),
        ('짜증', '짜증'),
        ('무난', '무난'),
    ]
    diary_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    tag = models.CharField(max_length=50)
    detail = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mood = models.CharField(max_length=50, choices=MOOD_CHOICES)

    def __str__(self):
        return self.title