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

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login as auth_login
# from django.contrib.auth import logout as auth_logout
# from django.contrib.auth.decorators import login_required
# from .forms import CustomUserCreationForm


# 회원가입 함수
# def signup(request):
#     if request.method == "POST":
#         signup_form = CustomUserCreationForm(request.POST)
#         if signup_form.is_valid():
#             user = signup_form.save()
#             auth_login(request, user)
#             return redirect("apps.accountbook:check", user.pk)
#     else:
#         signup_form = CustomUserCreationForm()
#     context = {
#         "signup_form": signup_form,
#     }
#     return render(request, "accounts/signup.html", context)


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access_token", access_token, httponly=True)
            res.set_cookie("refresh_token", refresh_token, httponly=True)
            return res
        return Response(status=status.HTTP_400_BAD_REQUEST)


# 로그인 함수
# def login(request):
#     if request.method == "POST":
#         login_form = AuthenticationForm(request, data=request.POST)
#         if login_form.is_valid():
#             user = login_form.get_user()
#             auth_login(request, user)
#             user_pk = user.pk
#             return redirect(
#                 request.GET.get("next") or "apps.accountbook:check", user_pk
#             )
#     else:
#         login_form = AuthenticationForm()
#     context = {
#         "login_form": login_form,
#     }
#     return render(request, "accounts/login.html", context)


# @login_required
# def logout(request):
#     auth_logout(request)
#     return redirect("apps.accounts:login")



# @login_required
# def profile(request, user_pk):
#     user = get_object_or_404(get_user_model(), pk=user_pk)
#     context = {
#         "user": user,
#     }
#     return render(request, "accounts/profile.html", context)


# 로그인, 로그아웃, 프로필페이지 기능 클래스뷰
class AuthAPIView(APIView):
    # 유저 식별
    def get(self, request):
        try:
            access_token = request.COOKIES["access_token"]
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
            print(payload)
            user_pk = payload.get("user_id")
            user = get_object_or_404(get_user_model(), pk=user_pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except jwt.exceptions.ExpiredSignatureError:
            # 토큰 만료
            data = {
                # 리프레시 토큰이 있으면 가져오고 없으면 기본 None
                "refresh_token": request.COOKIES.get("refresh_token", None),
            }
            serializer = TokenRefreshSerializer(data=data)
            # 리프레시 토근을 성공적으로 가져왔을때 실행
            if serializer.is_valid(raise_exception=True):
                access_token = serializer.data.get("access_token", None)
                refresh_token = serializer.data.get("refresh_token", None)
                payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
                user_pk = payload.get("user_id")
                user = get_object_or_404(get_user_model(), pk=user_pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie("access_token", access_token)
                res.set_cookie("refresh_token", refresh_token)
                return res
            raise jwt.exceptions.InvalidTokenError

        except jwt.exceptions.InvalidTokenError:
            # 사용 불가능한 토큰
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    def post(self, request):
        # 유저 인증
        user = authenticate(
            email=request.data.get("email"),
            password=request.data.get("password"),
        )
        # 유저 정보 있음
        if user:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access_token", access_token, httponly=True)
            res.set_cookie("refresh_token", refresh_token, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰을 삭제한다.
        response = Response(
            {
                "message": "Logout success",
            },
            status=status.HTTP_202_ACCEPTED,
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
