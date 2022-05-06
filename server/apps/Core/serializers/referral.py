from rest_framework import serializers

from server.apps.Account.serializers import UserSerializerReferral
from server.apps.Core.models import Referral


class ReferralSerializer(serializers.ModelSerializer):
    recruit = UserSerializerReferral(read_only=True)

    class Meta:
        model = Referral
        fields = ["id", "recruiter", "recruit", "time_stamp"]


