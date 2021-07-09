from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from Core.models import Referral
from Core.serializers.referral import ReferralSerializer
from Core.views.permissions import RecruiterOnlyPermission
from ShoreCapitalReferral.pagination import DefaultPaginationClass


class ReferralListApi(ListAPIView):
    permission_classes = [IsAuthenticated, RecruiterOnlyPermission]
    pagination_class = DefaultPaginationClass
    serializer_class = ReferralSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):

        return Referral.objects.filter(recruiter=self.request.user).order_by("id")
