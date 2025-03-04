from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# 사용자
class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

