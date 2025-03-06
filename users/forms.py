from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import User

# 회원가입 폼
class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Check', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields =["name","email","nickname","phone_number"]

        def __init__(self):
            self.cleaned_data = None

        def clean_password2(self):
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")

            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
            return password2

# 프로필 수정 폼
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "nickname", "phone_number"]