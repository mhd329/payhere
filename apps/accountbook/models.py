from django.db import models
from config.settings import AUTH_USER_MODEL
from django.utils import timezone


# Create your models here.


# 현지시각으로 저장해야하기 때문에 타임스탬프를 따로 만듦
class TimeStampedModel(models.Model):
    """
    최초 등록 시간은 수정할 수 없게 editable=False 했다.\n
    만든 시각이 UTC로 저장되는 것을 방지하기 위해 default=timezone.now 설정하였다.\n
    수정 시각은 기본 공백으로 두고 save메서드 호출 시 timezone.localtime() 을 통해 저장 당시의 현지 시각을 저장하도록 하였다.\n
    이 클래스는 추상 클래스 설정을 하였기 때문에 단독으로 사용할 수 없다.
    """

    created_at = models.DateTimeField(
        default=timezone.now, editable=False, verbose_name="최초로 등록된 시간"
    )
    updated_at = models.DateTimeField(
        null=True, blank=True, auto_now_add=False, verbose_name="마지막으로 수정된 시간"
    )

    # 추상클래스 설정을 함으로써 상속 없이는 사용할 수 없게 함
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = timezone.localtime()
        super().save(*args, **kwargs)


class UserAccount(TimeStampedModel):
    """
    유저는 가계부의 이름을 반드시 적어야 한다.\n
    가계부의 설명은 선택적으로 적을 수 있게 하였다.\n
    가계부의 잔액은 기본 0으로 두었다.
    """

    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    # balance로 명명했지만 total이라는 변수명이 좀 더 정확한 것 같다.
    balance = models.IntegerField(default=0)

    class Meta:
        db_table = "UserAccount"


class TodayHistory(TimeStampedModel):
    """
    기본키는 아래의 과정을 통해 구성된다.\n
    1. 모듈을 통해 현지 시각을 불러온다.\n
    2. 유저의 아이디에 불러온 연월일을 붙인다.\n
    3. 2의 뒷부분에 django AutoField로 생성된 숫자를 붙인다.\n
    django에서 기본으로 제공해주는 기본키를 사용하게 되면 AccountTotalHistory와 union할 때 키가 같게 되므로 새로 만들었다.
    """

    # 소비 유형은 카드나 현금으로 정해진다.
    CONSUMPTION_TYPE = (
        ("카드", "카드"),
        ("현금", "현금"),
    )
    MAIN_CATEGORY = (
        ("의류비", "의류비"),
        ("식비", "식비"),
        ("주거비", "주거비"),
        ("기타", "기타"),
    )
    consumption_type = models.CharField(
        max_length=2, choices=CONSUMPTION_TYPE, default="카드", verbose_name="소비유형"
    )
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(
        UserAccount, verbose_name="계좌", on_delete=models.CASCADE
    )
    # 수입과 지출 내역, 양수와 음수 여부로 수입과 지출을 구분한다.
    breakdown = models.IntegerField(default=0, verbose_name="액수")
    main_category = models.CharField(
        max_length=8, choices=MAIN_CATEGORY, default="기타", verbose_name="대분류"
    )
    sub_category = models.CharField(
        max_length=30, verbose_name="소분류", blank=True, null=True
    )
    memo = models.CharField(max_length=50, verbose_name="메모", blank=True, null=True)

    class Meta:
        db_table = "TodayHistory"


class AccountTotalHistory(TimeStampedModel):
    """
    TodayHistory 테이블과는 id 필드를 제외하고 완벽히 동일한 모델이다.\n
    id 필드가 다른 이유는 AccountTotalHistory 테이블은 따로 만들어지는 것이 아니라, 매일의 TodayHistory 데이터가 쌓여 union 되어가며 점차 누적되는 것이므로 서로 값을 합칠 수 있게 컬럼의 수만 같게 했다.\n
    TodayHistory의 id는 문자열화된 다음 앞에 uid와 날짜가 붙어 하루가 지날 때마다 이 테이블의 아랫 부분에 결합된다.\n
    예) uid + 20230405 + id == 1202304053
    """

    id = models.CharField(primary_key=True, max_length=255)
    CONSUMPTION_TYPE = (
        ("카드", "카드"),
        ("현금", "현금"),
    )
    MAIN_CATEGORY = (
        ("의류비", "의류비"),
        ("식비", "식비"),
        ("주거비", "주거비"),
        ("기타", "기타"),
    )
    consumption_type = models.CharField(
        max_length=2, choices=CONSUMPTION_TYPE, default="카드", verbose_name="소비유형"
    )
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(
        UserAccount, verbose_name="계좌", on_delete=models.CASCADE
    )
    breakdown = models.IntegerField(default=0, verbose_name="액수")
    main_category = models.CharField(
        max_length=8, choices=MAIN_CATEGORY, default="기타", verbose_name="대분류"
    )
    sub_category = models.CharField(
        max_length=30, verbose_name="소분류", blank=True, null=True
    )
    memo = models.CharField(max_length=50, verbose_name="메모", blank=True, null=True)

    class Meta:
        db_table = "AccountTotalHistory"
