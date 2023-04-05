# from rest_framework import viewsets, permissions, generics, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def signup(request):
    if request.method == "POST":
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            return redirect("apps.accountbook:my-accounts", user.pk)
    else:
        signup_form = CustomUserCreationForm()
    context = {
        "signup_form": signup_form,
    }
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            user_pk = user.pk
            return redirect(
                request.GET.get("next") or "apps.accountbook:my-accounts", user_pk
            )
    else:
        login_form = AuthenticationForm()
    context = {
        "login_form": login_form,
    }
    return render(request, "accounts/login.html", context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect("apps.accounts:login")


@login_required
def profile(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    context = {
        "user": user,
    }
    return render(request, "accounts/profile.html", context)
