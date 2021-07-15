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
    email_template = "forgot_password.html"

    # Post Method
    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        if email:
            try:
                # Get User Account Via Provided Email
                user = User.objects.get(email=email)
                # Initiate or Create a New Password Change Request
                fp_obj, created = self.model.objects.get_or_create(user=user)
                # Check if Client has sent request more than or equal REQUEST SENT THRESHOLD
                has_threshold_passed = fp_obj.request_sent >= fp_obj.MAXIMUM_REQUEST_SENT_THRESHOLD
                # Check if Forget Password Initialization has increased by MAXIMUM_REQUEST_SENT_WAIT_TIME
                time_delta = timezone.timedelta(minutes=fp_obj.MAXIMUM_REQUEST_SENT_WAIT_TIME)
                has_time_passed = timezone.now() > fp_obj.time_stamp + time_delta
                # If Client has passed the maximum request sent threshold and initial time has increased by wait time
                # Client can send else client can't send request
                can_request_with_threshold = has_time_passed and has_threshold_passed
                # If threshold has not passed or special logic
                if not has_threshold_passed or can_request_with_threshold:
                    # Set Expiration Time to initial time + 1 hour
                    fp_obj.expiration_time = timezone.now() + datetime.timedelta(hours=1)
                    # Sent Request Save
                    if fp_obj.request_sent >= fp_obj.MAXIMUM_REQUEST_SENT_THRESHOLD:
                        # Reset the request sent
                        fp_obj.request_sent = 1
                    else:
                        fp_obj.request_sent += 1
                    # Reset Link
                    fp_obj.unique_link = get_random_string(30)
                    # Save Object
                    fp_obj.save()
                    # Send Email
                    SendEmail.send_html_email(
                        template=self.email_template,
                        subject="Shore Capital Agent Referral Password Reset",
                        to=fp_obj.user.email,
                        body=get_forget_password_message(fp_obj.unique_link)
                    )
                    # User Email as Secret
                    email = fp_obj.user.email
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
                    return Response({"msg": 1, "text": "Valid Code"}, status=status.HTTP_200_OK)
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
