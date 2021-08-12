from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from Core.models import Referral
from Core.serializers.referral import ReferralSerializer
from Core.views.permissions import RecruiterOnlyPermission
from ShoreCapitalReferral.pagination import DefaultPaginationClass


class ReferralListApi(ListAPIView):
    """
    URL : api/core/referral/?page=<Page Number>
    Headers: Token
    Returns : {
        next:
        prev:
        results: [
            {
                recruit: {
                    first_name: "",
                    last_name: "",
                    email: ""
                },
                time_stamp: <DATE>
            }
        ]
    }
    """
    permission_classes = [IsAuthenticated, RecruiterOnlyPermission]
    pagination_class = DefaultPaginationClass
    serializer_class = ReferralSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Referral.objects.select_related("recruit").filter(recruiter=self.request.user).order_by("id")
