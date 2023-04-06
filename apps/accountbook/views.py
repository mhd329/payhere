import jwt
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from config.settings import SECRET_KEY
from django.contrib.auth import get_user_model

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from .models import *
from .forms import *
import json


@login_required
def check(request, user_pk):
    return redirect("apps.accountbook:my-accounts", user_pk)


@login_required
def history(request, user_pk, account_pk):
    if request.user.pk == user_pk:
        account = get_object_or_404(UserAccount, user_id=user_pk, pk=account_pk)
        make_history_form = MakeHistoryForm()
        today_account_history = History.objects.filter(
            account_id=account_pk, user_id=user_pk
        )
        if request.method == "POST":
            make_history_form = MakeHistoryForm(request.POST)
            if make_history_form.is_valid():
                new_history = make_history_form.save(commit=False)
                new_history.user_id = user_pk
                new_history.account_id = account_pk
                new_history.account.balance += new_history.breakdown
                new_history.account.save()
                new_history.save()
            # 양식 다시 제출을 방지하기 위해 리다이렉트 시킴
            return redirect(f"/accountbook/history/{user_pk}/{account_pk}/")
        else:
            make_history_form = MakeHistoryForm()
        context = {
            "today_account_history": today_account_history
            if today_account_history
            else None,
            "make_history_form": make_history_form,
            "account_pk": account_pk,
            "account": account,
            "user_pk": user_pk,
        }
        return render(request, "accountbook/history.html", context)


@login_required
def update(request, user_pk, account_pk, object_pk):
    if request.user.pk == user_pk:
        target_history = get_object_or_404(
            History, pk=object_pk, user_id=user_pk, account_id=account_pk
        )
        old = target_history.breakdown
        if request.method == "POST":
            update_form = MakeHistoryForm(request.POST, instance=target_history)
            if update_form.is_valid():
                updated_history = update_form.save(commit=False)
                new = updated_history.breakdown
                if new != old:
                    new - old
                    updated_history.account.balance += new - old
                updated_history.account.save()
                updated_history.save()
                return redirect(f"/accountbook/history/{user_pk}/{account_pk}/")
        else:
            update_form = MakeHistoryForm(instance=target_history)
        context = {
            "update_form": update_form,
            "account_pk": account_pk,
            "user_pk": user_pk,
        }
        return render(request, "accountbook/update.html", context)


@login_required
def remove(request, user_pk, account_pk, object_pk):
    if request.user.pk == user_pk:
        target_history = get_object_or_404(
            History, pk=object_pk, user_id=user_pk, account_id=account_pk
        )
        target_history.account.balance -= target_history.breakdown
        target_history.account.save()
        target_history.delete()
        return redirect(f"/accountbook/history/{user_pk}/{account_pk}/")


@login_required
def share(request, user_pk, account_pk, object_pk):
    return


@login_required
def my_accounts(request, user_pk):
    if request.user.pk == user_pk:
        user_accounts = UserAccount.objects.filter(user_id=user_pk)
        if user_accounts:
            context = {
                "user_accounts": user_accounts,
            }
        else:
            context = {
                "user_accounts": None,
            }
        return render(request, "accountbook/my-accounts.html", context)


class AuthAPIView(APIView):
    def get(self, request):
        try:
            access_token = request.COOKIES["access_token"]
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
            print(payload)
            user_pk = payload.get("user_id")
            user = get_object_or_404(get_user_model(), pk=user_pk)
            serializer = UserAccountSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except jwt.exceptions.ExpiredSignatureError:
            # 토큰 만료
            return Response(status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.InvalidTokenError:
            # 사용 불가능한 토큰
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = {
            "title": request.data.get("title"),
            "description": request.data.get("description", None),
            "balance": request.data.get("balance", 0),
            "user": request.user.id,
        }
        serializers = UserAccountSerializer(data=data)
        if serializers.is_valid():
            serializers.save()


@login_required
def make_account(request, user_pk):
    if request.user.pk == user_pk:
        if request.method == "POST":
            make_account_form = MakeMyAccountForm(request.POST)
            user = get_object_or_404(get_user_model(), pk=user_pk)
            if make_account_form.is_valid():
                user_account = make_account_form.save(commit=False)
                user_account.user = user
                user_account.save()
                return redirect("apps.accountbook:my-accounts", user_pk)
        else:
            make_account_form = MakeMyAccountForm()
        context = {
            "make_account_form": make_account_form,
        }
        return render(request, "accountbook/make-account.html", context)


@login_required
def remove_account(request, user_pk, account_pk):
    if request.user.pk == user_pk:
        if request.method == "POST":
            my_account = get_object_or_404(UserAccount, user_pk=user_pk)
            my_account.delete()
            return redirect("accountbook/my-accounts.html", user_pk)
        else:
            return render(request, "accountbook/remove-account.html")
