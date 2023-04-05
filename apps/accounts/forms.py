from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)

    # 가입 시 비밀번호 입력란 하단에 나오는 helptext가 보기 싫어서 없애주는 코드
    # 상속 받고있는 UserCreationForm에 직접 접근해서 password1과 2의 helptext를 지워줘도 되지만, 재정의를 통해 없앨 수 있는 방법이다.
    # 자세한 원리는 잘 모르겠다.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ("password1", "password2"):
            self.fields[field].help_text = ""
