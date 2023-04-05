# from rest_framework import viewsets, permissions, generics, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from .models import *
from .forms import *
from django.urls import reverse


# pk를 구성하는 조각을 만들어주는 함수
def key_generate():
    now = str(timezone.localtime())
    arr = now.replace("-", "").split()
    return arr[0]


# totalhistory.id = str(user_pk) + key_generate() + str(todayhistory.id)


@login_required
def day(request, user_pk, account_pk):
    account = get_object_or_404(UserAccount, user_id=user_pk, pk=account_pk)
    make_history_form = MakeHistoryForm()
    today_account_history = TodayHistory.objects.filter(
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
        return redirect(f"/accountbook/day/{user_pk}/{account_pk}/")
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
    return render(request, "accountbook/day.html", context)


@login_required
def update(request, user_pk, account_pk, object_pk):
    target_history = get_object_or_404(
        TodayHistory, pk=object_pk, user_id=user_pk, account_id=account_pk
    )
    target_history
    return redirect(f"/accountbook/day/{user_pk}/{account_pk}/")


@login_required
def delete(request, user_pk, account_pk, object_pk):
    target_history = get_object_or_404(
        TodayHistory, pk=object_pk, user_id=user_pk, account_id=account_pk
    )
    target_history.account.balance -= target_history.breakdown
    target_history.account.save()
    target_history.delete()
    return redirect(f"/accountbook/day/{user_pk}/{account_pk}/")


@login_required
def month(request, user_pk, account_pk):
    return render(request, "accountbook/month.html")


@login_required
def year(request, user_pk, account_pk):
    return render(request, "accountbook/year.html")


@login_required
def history(request, user_pk, account_pk):
    return render(request, "accountbook/history.html")


@login_required
def my_accounts(request, user_pk):
    # user = get_object_or_404(get_user_model(), pk=user_pk)
    user_accounts = UserAccount.objects.filter(user_id=user_pk)
    if user_accounts:
        context = {
            "user_accounts": user_accounts,
        }
    else:
        context = {
            "user_accounts": None,
        }
    print(user_accounts)
    return render(request, "accountbook/my-accounts.html", context)


@login_required
def make_account(request, user_pk):
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
def delete_account(request, user_pk, account_pk):
    if request.method == "POST":
        my_account = get_object_or_404(UserAccount, user_pk=user_pk)
        my_account.delete()
        return redirect("accountbook/my-accounts.html", user_pk)
    else:
        return render(request, "accountbook/delete-account.html")
