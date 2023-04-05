from django.urls import path
from . import views

app_name = "apps.accountbook"

urlpatterns = [
    path("my-accounts/<int:user_pk>/", views.my_accounts, name="my-accounts"),
    path("make-account/<int:user_pk>/", views.make_account, name="make-account"),
    path(
        "delete-account/<int:user_pk>/<int:account_pk>/",
        views.delete_account,
        name="delete-account",
    ),
    path("history/<int:user_pk>/<int:account_pk>/", views.history, name="history"),
    path("day/<int:user_pk>/<int:account_pk>/", views.day, name="day"),
    path("month/<int:user_pk>/<int:account_pk>/", views.month, name="month"),
    path("year/<int:user_pk>/<int:account_pk>/", views.year, name="year"),
    path(
        "day/<int:user_pk>/<int:account_pk>/delete/<str:object_pk>/",
        views.delete,
        name="delete",
    ),
    path(
        "day/<int:user_pk>/<int:account_pk>/update/<str:object_pk>/",
        views.update,
        name="update",
    ),
]
