from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from Core.models.transaction import Commission
from Core.serializers.referral import ReferralSerializer
from Core.views.permissions import RecruiterOnlyPermission
from ShoreCapitalReferral.pagination import DefaultPaginationClass


# Returns Commission List
class CommissionListApi(ListAPIView):
    """
    URL : api/core/recruiter/commission/?page=<Page Number>
    Headers: Token
    Returns : {
        next:
        prev:
        results: [
            {
                transaction: 1,
                commission: 100,
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
    # Permission Class
    permission_classes = [IsAuthenticated, RecruiterOnlyPermission]
    pagination_class = DefaultPaginationClass
    serializer_class = ReferralSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Commission.objects.filter(recruiter=self.request.user).order_by("id")