from django.urls import path

from Account.views import AuthApi, ChangePasswordApi, AccountUpdateApi, CheckEmailAvailableApi

urlpatterns = [
    path("login/", AuthApi.as_view(), name="login"),
    path("change-password/", ChangePasswordApi.as_view(), name="change-password"),
    path("user/update/", AccountUpdateApi.as_view(), name="user-update"),
    path("user/email/check", CheckEmailAvailableApi.as_view(), name="email-check")
]