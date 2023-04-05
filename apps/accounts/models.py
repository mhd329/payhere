from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일을 입력해주세요.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password=password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name="이메일",
        unique=True,
        validators=[validate_email],
        error_messages={"unique": "이미 가입된 이메일입니다."},
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="가입일",
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name="관리자 여부",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # 이메일을 기본으로 출력함
    def __str__(self):
        return self.email

    # CustomUserManager를 사용하여 User모델의 objects매니저를 재정의함
    objects = CustomUserManager()

    class Meta:
        db_table = "User"
