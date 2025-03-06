from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):

    list_display = (
        "name",
        "nickname",
        "email",
        "last_login",
    )
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "nickname", "phone_number")
    ordering = ("email",)
    fieldsets = (
        (
            "User Info",
            {"fields": ("nickname", "email", "phone_number")},
        ),  # 사용자의 기본정보 표시
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "is_superuser")},
        ),  # 권한 관련 필드 표시
    )

    readonly_fields = ("last_login", "is_superuser")  # 읽기 전용 필드

    add_fieldsets = (
        (
            "New user",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "nickname",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )
