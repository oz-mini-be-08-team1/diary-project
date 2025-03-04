from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# 사용자
class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=50)
