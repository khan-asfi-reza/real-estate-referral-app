from django.urls import path
from Core.views.referral import ReferralListApi
from Core.views.referred import ReferredUserCreateListApi, ReferredUserCRUDApi
from Core.views.recruiter import RecruiterCreateApi, RecruiterCRUDApi, RefCodeApi, RecruiterInfographicApi

view_perms = {
        "put": "partial_update",
        "get": "retrieve",
        "delete": "destroy"
}


urlpatterns = [
    path("ref-code/", RefCodeApi.as_view(), name="ref-code"),
    path("recruiter/", RecruiterCRUDApi.as_view(), name="recruiter-crud"),
    path("recruiter/create", RecruiterCreateApi.as_view(), name="recruiter-create"),
    path("referred/", ReferredUserCreateListApi.as_view(), name="referred-create-list"),
    path("referred/<int:pk>", ReferredUserCRUDApi.as_view(view_perms), name="referred-crud"),
    path("referral/", ReferralListApi.as_view(), name="referral-list"),
    path("recruiter/info", RecruiterInfographicApi.as_view(), name="recruiter-info")
]

