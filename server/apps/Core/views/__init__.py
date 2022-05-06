from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from server.apps.Account.serializers import UserSerializer


def get_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token


class UserNestedCreateApi(CreateAPIView):
    user_serializer = UserSerializer
    role = None

    @staticmethod
    def send_bad_request(*args):
        for error in args:
            if error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def create_user(self, request, *args, **kwargs):
        """
        Returns user and error, if user is created it returns user without error
        """
        user = request.data.get("user", None)
        if user is not None:
            # If User, save base user
            user = self.user_serializer(data=user)
            if user.is_valid():
                # Save
                user = user.save(role=self.role)
                return user, None
            # Return User Error
            return None, user.errors
        return None, {"error": ["Invalid User"]}

    def create_model_data(self, request, *args, **kwargs):

        """
        Create Model Data returns the model unsaved object, Error,
        If the serializer has no error, it returns the unsaved object, and None,
        otherwise it returns none and error
        """
        # Create Required Data Object
        __obj = self.serializer_class(data=request.data)
        # If object is valid
        if __obj.is_valid():
            return __obj, None
        # Return Error
        return None, __obj.errors

    def create(self, request, *args, **kwargs):
        # Gets model object
        obj, error = self.create_model_data(request, *args, **kwargs)
        # Gets user
        user, user_error = self.create_user(request, *args, **kwargs)
        # Valid user and model object

        if obj and user:
            # Saves object
            obj.save(user=user)
            token = get_token(user)
            # Return Object
            return Response({
                "token": token.key,
                "data": obj.data,
            },
                status=status.HTTP_201_CREATED)
        # Return Error
        return self.send_bad_request(error, user_error, {"error": ["Invalid user error"]})

