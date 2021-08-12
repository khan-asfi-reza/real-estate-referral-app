from django.contrib import admin
from django.urls import path
from Core.views.referral import ReferralListApi
from Core.views.recruit import RecruitUserCreateListApi, RecruitUserCRUDApi
from Core.views.recruiter import RecruiterCreateApi, RecruiterCRUDApi, RefCodeApi, RecruiterInfographicApi
from Core.views.transaction import CommissionListApi

view_perms = {
    "put": "partial_update",
    "get": "retrieve",
    "delete": "destroy"
}

urlpatterns = [
    path("ref-code/", RefCodeApi.as_view(), name="ref-code"),
    path("recruiter/", RecruiterCRUDApi.as_view(), name="recruiter-crud"),
    path("recruiter/create", RecruiterCreateApi.as_view(), name="recruiter-create"),
    path("recruit/", RecruitUserCreateListApi.as_view(), name="recruit-create-list"),
    path("recruit/<int:pk>", RecruitUserCRUDApi.as_view(view_perms), name="recruit-crud"),
    path("referral/", ReferralListApi.as_view(), name="referral-list"),
    path("recruiter/info", RecruiterInfographicApi.as_view(), name="recruiter-info"),
    path("recruiter/commission", CommissionListApi.as_view(), name="commission-list")
]

admin.site.site_header = "Shore Capital Agent Referral"
admin.site.site_title = "Shore Capital Agent Referral"
admin.site.index_title = "Shore Capital Agent Referral"
