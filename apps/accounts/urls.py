from django.urls import path, include
from .views import *

app_name = "apps.accounts"

urlpatterns = [
    # path("signup/", views.signup, name="signup"),
    path("registration/", RegisterAPIView.as_view()),
    # path("login/", views.login, name="login"),
    # path("logout/", views.logout, name="logout"),
    # path("profile/<int:user_pk>/", profile, name="profile"),
    path("auth/", AuthAPIView.as_view()),
]
