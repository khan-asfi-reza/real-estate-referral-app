from rest_framework import serializers
from server.apps.Core.models.recruit import Recruit
from server.apps.Account.serializers import UserSerializer


# Referred Serializer
class RecruitSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Recruit
        fields = ["id", "user", "nmls_number", "dre_license", ]
        read_only_fields = ("id",)
