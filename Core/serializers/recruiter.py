from django.contrib.auth import get_user_model
from rest_framework import serializers
from Core.models import Recruiter
from Account.serializers import UserSerializer

User = get_user_model()


# Referrer Serializer
class RecruiterSerializer(serializers.ModelSerializer):
    # Nested User Serializer
    user = UserSerializer(read_only=True)

    class Meta:
        model = Recruiter
        fields = "__all__"
        read_only = ("id",)


# Recruiter Ref Code Serializer
class RecruiterRefCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recruiter
        fields = ["id", "ref_code"]
        read_only = ("id", )