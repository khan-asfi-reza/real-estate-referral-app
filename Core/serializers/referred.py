from rest_framework import serializers
from Core.models.referred import Referred
from Core.serializers.recruiter import RecruiterSerializer
from Account.serializers import UserSerializer


# Referred Serializer
class ReferredSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Referred
        fields = ["id", "user", "nmls_number", "dre_license", ]
        read_only_fields = ("id",)
