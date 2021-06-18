from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

User = get_user_model()


# Authenticate User Using name and password, returns validated user data after authentication
class AuthenticationSerializer(serializers.Serializer):
    # Username
    email = serializers.CharField(required=True, trim_whitespace=True)
    # Password
    password = serializers.CharField(required=True,
                                     style={'input_type': 'password'},
                                     trim_whitespace=False)

    # Validate username and password, returns Auth User
    def validate(self, attrs):
        # Validate and authenticate
        email = attrs.get('email')
        password = attrs.get('password')
        # If user not exist return error
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Account does not exist'}, code='authentication')
        # Authenticate user
        user = authenticate(request=self.context.get('request'),
                            username=email,
                            password=password)
        # If user error send error
        if not user:
            msg = "Username or password is wrong"
            raise serializers.ValidationError({'error': msg}, code='authentication')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


# Change Password Serializer
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True,
                                         style={'input_type': 'password'},
                                         trim_whitespace=False)
    new_password = serializers.CharField(required=True,
                                         style={'input_type': 'password'},
                                         trim_whitespace=False)

    # Validates OLD password
    def validate(self, attrs):
        request = self.context.get('request')
        old_password = attrs.get('old_password')
        if not request.user.check_password(old_password):
            raise serializers.ValidationError({"error": ["Old password is wrong"]})
        return attrs

    # Create new password
    def create(self, validated_data):
        user = self.context.get('request').user
        user.set_password(validated_data.get('new_password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):
    # User Model Serializer
    class Meta:
        model = User
        fields = ["id", "email", "password", "phone_number","first_name", "last_name", "city", "state", "zip", "address", "role"]
        extra_kwargs = {
            "password": {"write_only": True}
        }
        read_only_fields = ("id", "date_joined", "last_login", "role")


# User serializer for referral views
class UserSerializerReferral(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]