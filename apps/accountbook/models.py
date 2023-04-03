from django.db import models
from config.settings import AUTH_USER_MODEL


# Create your models here.


class UserAccount(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)


class TodayHistory(models.Model):
    MAIN_CATEGORY = (
        ("clothing", "의류비"),
        ("food", "식비"),
        ("shelter", "주거비"),
        ("general", "기타"),
    )
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(
        UserAccount, verbose_name="계좌", on_delete=models.CASCADE
    )
    breakdown = models.IntegerField(default=0, verbose_name="액수")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록된 시간")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="마지막으로 수정된 시간")
    main_category = models.CharField(
        max_length=8, choices=MAIN_CATEGORY, default="general", verbose_name="대분류"
    )
    sub_category = models.CharField(
        max_length=30, verbose_name="소분류", blank=True, null=True
    )
    memo = models.CharField(max_length=50, verbose_name="메모", blank=True, null=True)


class AccountTotalHistory(models.Model):
    MAIN_CATEGORY = (
        ("clothing", "의류비"),
        ("food", "식비"),
        ("shelter", "주거비"),
        ("general", "기타"),
    )
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(
        UserAccount, verbose_name="계좌", on_delete=models.CASCADE
    )
    breakdown = models.IntegerField(default=0, verbose_name="액수")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록된 시간")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="마지막으로 수정된 시간")
    main_category = models.CharField(
        max_length=8, choices=MAIN_CATEGORY, default="general", verbose_name="대분류"
    )
    sub_category = models.CharField(
        max_length=30, verbose_name="소분류", blank=True, null=True
    )
    memo = models.CharField(max_length=50, verbose_name="메모", blank=True, null=True)
