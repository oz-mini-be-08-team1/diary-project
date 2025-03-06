from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "name", "nickname", "password"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "nickname", "password"]

        def create(self, validated_data):
            user = User(
                email=validated_data["email"],
                name=validated_data["name"],
                nickname=validated_data["nickname"],
            )

            user.set_password(validated_data["password"])  # 비밀번호 암호화
            user.save()
            return user
