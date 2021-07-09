import datetime
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from Account.models import ForgetPassword
from Account.send_email import SendEmail, get_forget_password_message
from Account.serializers import PasswordChangeSerializer

User = get_user_model()


class ChangePasswordApi(GenericAPIView):
    # Change Password
    serializer_class = PasswordChangeSerializer
    # Authentication Class
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Post Request to change password
    def post(self, request, *args, **kwargs):
        # Get serialized data
        serialized_data = self.get_serializer(data=request.data)
        # Save user password
        if serialized_data.is_valid():
            user = serialized_data.save()
            # Create new token
            token = Token.objects.filter(user=user)
            if token.exists():
                token.first().delete()
            new_token = Token.objects.create(user=user)
            return Response({
                "token": new_token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordApi(APIView):
    model = ForgetPassword

    # Post Method
    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        if email:
            try:
                # Get User
                user = User.objects.get(email=email)
                forget_pass_obj, created = self.model.objects.get_or_create(user=user)
                # If User sent request 5 times and
                # 20 minutes since initiated time has not been passed the user will have to wait until 20 minutes
                if forget_pass_obj.request_sent != forget_pass_obj.REQUEST_SENT_THRESHOLD:
                    if forget_pass_obj.time_stamp + timezone.timedelta(minutes=20) > timezone.now():
                        # Set Expiration Time
                        forget_pass_obj.expiration_time = timezone.now() + datetime.timedelta(hours=1)
                        # Sent Request Save
                        if forget_pass_obj.request_sent == forget_pass_obj.REQUEST_SENT_THRESHOLD:
                            forget_pass_obj.request_sent = 1
                        else:
                            forget_pass_obj.request_sent += 1
                        # Reset Link
                        forget_pass_obj.unique_link = get_random_string(30)
                        # Save Object
                        forget_pass_obj.save()
                        SendEmail.send_email(
                            subject="Shore Capital Agent Referral Password Reset",
                            to=forget_pass_obj.user.email,
                            body=get_forget_password_message(forget_pass_obj.unique_link)
                        )
                        email = forget_pass_obj.user.email
                        secret_email = email[0:4] + "*" * (len(email.split('@')[0]) - 3) + f"@{email.split('@')[1]}"

                        return Response({
                            "msg": 1,
                            "text": f"An email has been sent to "
                                    f"{secret_email}"
                        }, status=status.HTTP_201_CREATED)

                return Response({
                    "msg": 0,
                    "text": "Too many request sent, please wait for 20 minutes"
                }, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": ["No Account registered with this email"]},
                                status=status.HTTP_400_BAD_REQUEST)


class ValidateResetLink(APIView):
    fp_model = ForgetPassword

    def post(self, request, *args, **kwargs):
        # Unique Link and Password
        unique_link = request.data.get("unique_link", "")
        # If Valid Unique Link
        if unique_link:
            # Try Getting Forget Password Model data using unique link
            fp_data = self.fp_model.objects.filter(unique_link=unique_link)
            if fp_data.exists():
                # Return Validation Code
                if fp_data.first().expiration_time >= timezone.now():
                    return Response({"msg": 1, "text": "Valid Code"})
        # Return Error
        return Response({"msg": 0, "error": ["Invalid link"]}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordApi(APIView):
    user_model = User
    fp_model = ForgetPassword

    @staticmethod
    def return_error():
        return Response({
            "msg": 0,
            "text": "The link you have used either expired or does not exist"
        },
            status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        # Unique Link and Password
        unique_link = self.request.data.get("unique_link", "")
        password = self.request.data.get("password", "")
        email = self.request.data.get("email", "")
        # If Valid Unique Link and Password available
        if unique_link and password and email:
            # Try Getting Forget Password Model data using unique link
            try:
                fp_data = self.fp_model.objects.get(unique_link=unique_link, user__email=email)
                if fp_data.expiration_time >= timezone.now():
                    # Get User and set password
                    fp_data.user.set_password(password)
                    # Save Password
                    fp_data.user.save()
                    # Delete Forget Password
                    fp_data.delete()
                    return Response({"msg": 1, "text": "Password has been changed, please login to enter"},
                                    status=status.HTTP_201_CREATED)
                # If expired Return Error
                return self.return_error()
            except self.fp_model.DoesNotExist:
                return self.return_error()
