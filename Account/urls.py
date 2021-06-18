from django.urls import path

from Account.views import AuthApi, ChangePasswordApi, AccountUpdateApi

urlpatterns = [
    path("login/", AuthApi.as_view(), name="login"),
    path("change-password/", ChangePasswordApi.as_view(), name="change-password"),
    path("user/update/", AccountUpdateApi.as_view(), name="user-update")
]