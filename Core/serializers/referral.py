from rest_framework import serializers

from Account.serializers import UserSerializerReferral
from Core.models import Referral


class ReferralSerializer(serializers.ModelSerializer):
    recruit = UserSerializerReferral(read_only=True)

    class Meta:
        model = Referral
        fields = ["id", "recruiter", "recruit", "commission", "time_stamp"]
