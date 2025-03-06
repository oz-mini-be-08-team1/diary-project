from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from users.models import User
from Diary_Project import settings


def send_verification_email(user: User):
    token = default_token_generator.make_token(user)
    ver_link = f"http://127.0.0.1:8000/users/verify-email/?token={token}&email={user.email}"

    send_mail("이메일 인증 요청",
        f"아래 링크를 클릭하여 이메일을 인증하세요: {ver_link}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
