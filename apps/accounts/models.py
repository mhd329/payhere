from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class User(AbstractBaseUser):
    user_email = models.EmailField(
        error_messages={"unique": "이미 존재하는 이메일입니다."},
        help_text="이메일을 입력해주세요.",
        max_length=100,
        unique=True,
        validators=[validate_email],
        verbose_name="이메일 아이디",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="가입일",
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name="관리자 여부",
    )
    USERNAME_FIELD = "user_email"

    # 유저의 이메일 아이디를 기본으로 출력함
    def __str__(self):
        return self.user_email

    #
    class Meta:
        db_table = "User"
