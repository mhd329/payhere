from django import forms
from .models import *


class MakeMyAccountForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = (
            "title",
            "description",
            "balance",
        )

        labels = {
            "title": "가계부 이름",
            "description": "용도",
            "balance": "초기 총액",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "가계부 이름을 정해주세요. (필수 입력사항)",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "placeholder": "용도를 설정해주세요. (선택 입력사항, 생활비 가계부, 용돈 가계부 등)",
                }
            ),
            "balance": forms.NumberInput(
                attrs={
                    "placeholder": "총액을 설정해주세요. (필수 입력사항, 기본 0원으로 설정됩니다.)",
                }
            ),
        }


class MakeHistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = (
            "consumption_type",
            "main_category",
            "sub_category",
            "breakdown",
            "memo",
        )

        labels = {
            "consumption_type": "소비유형",
            "main_category": "대분류",
            "sub_category": "소분류",
            "breakdown": "변동액",
            "memo": "주석",
        }

        widgets = {
            "sub_category": forms.TextInput(
                attrs={
                    "placeholder": "소분류를 작성해주세요. (선택 사항)",
                }
            ),
            "breakdown": forms.NumberInput(
                attrs={
                    "placeholder": "변동액을 설정해주세요. (필수 입력사항, 기본 0원)",
                }
            ),
            "memo": forms.Textarea(
                attrs={
                    "style": "height: 4rem; resize: none;",
                }
            ),
        }
