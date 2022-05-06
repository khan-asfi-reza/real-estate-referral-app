from django.urls import path
from server.apps.Account.views.accounts import AuthApi, AccountUpdateApi, CheckEmailAvailableApi
from server.apps.Account.views.password import ChangePasswordApi, ForgetPasswordApi, ValidateResetLink, ResetPasswordApi

urlpatterns = [
    path("login/", AuthApi.as_view(), name="login"),
    path("user/update/", AccountUpdateApi.as_view(), name="user-update"),
    path("user/email/check", CheckEmailAvailableApi.as_view(), name="email-check"),
    path("password/change", ChangePasswordApi.as_view(), name="change-password"),
    path("password/forget", ForgetPasswordApi.as_view(), name="forget-password"),
    path("password/forget/validate", ValidateResetLink.as_view(), name="validate-reset-link"),
    path("password/reset", ResetPasswordApi.as_view(), name="reset-password")
]