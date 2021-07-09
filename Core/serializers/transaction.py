from rest_framework import serializers

from Account.serializers import UserSerializerReferral
from Core.models.transaction import Commission


class CommissionListSerializer(serializers.ModelSerializer):
    recruit = UserSerializerReferral(read_only=True)

    class Meta:
        model = Commission
        fields = ["id", "transaction", "commission", "recruit", "time_stamp"]


