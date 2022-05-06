from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from server.apps.Core.models import Recruiter, Referral
from server.apps.Core.models.transaction import Commission
from server.apps.Core.serializers.recruiter import RecruiterSerializer, RecruiterRefCodeSerializer
from server.apps.Core.views import UserNestedCreateApi
from server.apps.Core.views.permissions import RecruiterOnlyPermission

from django.db.models import Sum


# Recruiter Create Api
class RecruiterCreateApi(UserNestedCreateApi):
    model = Recruiter
    serializer_class = RecruiterSerializer
    role = 1


class RecruiterCRUDApi(GenericAPIView):
    """
        Get Method Only returns unique ref code
    """
    permission_classes = [IsAuthenticated, RecruiterOnlyPermission]
    authentication_classes = [TokenAuthentication]
    model = Recruiter
    serializer_class = RecruiterRefCodeSerializer
    queryset = Recruiter.objects.select_related("user").all()

    def get(self, request):
        # Recruiter Model
        try:
            recruiter = self.queryset.get(user=request.user)
            # Recruiter Serializer
            serialized_data = self.get_serializer(instance=recruiter)
            # Return Response
            return Response(serialized_data.data, status=status.HTTP_200_OK)

        except self.model.DoesNotExist:
            return Response({"error": "Error Ref Code"}, status=status.HTTP_400_BAD_REQUEST)


class RefCodeApi(APIView):

    def post(self, request, *args, **kwargs):
        # Recruiter Data
        ref_code = self.request.data.get("ref_code", None)

        if ref_code:
            # Recruiter User
            recruiter = Recruiter.objects.get_recruiter(ref_code)
            if recruiter:
                return Response({
                    "email": recruiter.email,
                    "full_name": recruiter.full_name
                })

            return Response({"error": ["Invalid Recruiter"]}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": ["Invalid Ref Code"]}, status=status.HTTP_400_BAD_REQUEST)


class RecruiterInfographicApi(APIView):
    permission_classes = [IsAuthenticated, RecruiterOnlyPermission]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        # Get Recruiter infographic
        ref_data = Referral.objects.filter(recruiter=self.request.user)
        # Total Recruited
        recruited = ref_data.count()
        # Total Bonus
        bonus = Commission.objects.filter(recruiter=self.request.user).aggregate(Sum("commission"))["commission__sum"]
        bonus = 0 if bonus is None else bonus

        return Response({
            "bonus": bonus,
            "total_recruited": recruited
        }, status=status.HTTP_200_OK)
