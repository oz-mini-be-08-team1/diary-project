from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# 유저 관리자 매니저
class UserManager(BaseUserManager):
    # 일반 사용자 생성 함수
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일을 입력해주세요.")
        email = self.normalize_email(email)  # 소문자 변환
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 (superuser) 생성 함수
    def create_superuser(self, email, name, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(email, name, password, **extra_fields)


# 커스텀 유저 모델
class User(AbstractUser):
    email = models.EmailField(unique=True)  # 로그인 시 사용
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=128)
    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)  # 활성화 여부
    is_superuser = models.BooleanField(default=False)  # 최고 관리자 여부
    is_staff = models.BooleanField(default=False)  # 관리자스탭 여부

    # 장고 기본 유저모델과 충돌 방지
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
    )
    objects = UserManager()

    USERNAME_FIELD = "email"  # 로그인에 사용할 필드
    REQUIRED_FIELDS = ["nickname", "name"]  # 슈퍼유저 생성시 필수 필드

    def __str__(self):
        return self.email
