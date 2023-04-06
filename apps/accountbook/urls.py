from django.urls import path
from .views import *

app_name = "apps.accountbook"

urlpatterns = [
    # path("<int:user_pk>/", views.check, name="check"),
    # path("my-accounts/<int:user_pk>/", my_accounts, name="my-accounts"),
    # path("make-account/<int:user_pk>/", make_account, name="make-account"),
    path("auth/", AuthAPIView.as_view()),
    path(
        "remove-account/<int:user_pk>/<int:account_pk>/",
        remove_account,
        name="remove-account",
    ),
    path("history/<int:user_pk>/<int:account_pk>/", history, name="history"),
    path(
        "day/<int:user_pk>/<int:account_pk>/remove/<int:object_pk>/",
        remove,
        name="remove",
    ),
    path(
        "day/<int:user_pk>/<int:account_pk>/share/<int:object_pk>/",
        share,
        name="share",
    ),
    path(
        "day/<int:user_pk>/<int:account_pk>/update/<int:object_pk>/",
        update,
        name="update",
    ),
]
