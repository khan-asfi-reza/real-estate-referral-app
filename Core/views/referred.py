from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from Core.models import Referred, Recruiter, Referral
from Core.serializers.referred import ReferredSerializer
from Core.views import UserNestedCreateApi, get_token


# Referred Create View
class ReferredUserCreateListApi(UserNestedCreateApi, ListAPIView):
    """
    URL: licensee/
    Method: Post, Get(List)
    Post Method:
        data: {
            user:{
                username: str,
                password: str,
                email: str,
                first_name: str,
                last_name: str
            },
            phone_number: str,
            nmls_number: str,
            dre_license: str,
            ref_code: str
        }

        Returns Saved Data

    List Method:
        Returns List of Referred

    """
    model = Referred
    serializer_class = ReferredSerializer
    ref_code_kwargs = "ref_code"
    queryset = Referred.objects.get_queryset()
    role = 2

    def get_recruiter(self, request):
        # Get ref code
        ref_code = request.data.get(self.ref_code_kwargs, None)
        if ref_code is not None:
            # Get recruiter detail from ref_code
            return Recruiter.objects.get_recruiter(ref_code), None

        return None, {"error": ["Invalid Ref Code"]}

    def create(self, request, *args, **kwargs):
        # Get User
        user, user_error = self.create_user(request, *args, **kwargs)
        # Get Referred Model Data
        obj, error = self.create_model_data(request, *args, **kwargs)
        # Referrer
        recruiter, ref_error = self.get_recruiter(request)

        if user and obj and recruiter:
            # Save Referred User
            obj.save(user=user)
            # Create referral object
            Referral.objects.create(referred=user, recruiter=recruiter)
            # Token
            token = get_token(user)
            return Response({
                "token": token.key,
                "data": obj.data,
            },
            status=status.HTTP_201_CREATED)

        return self.send_bad_request(user_error,
                                     ref_error, error,
                                     {"error": ["Invalid User Error"]},
                                     {"error": ["Invalid Referrer"]})


# Referred Retrieve Update Destroy View
class ReferredUserCRUDApi(ModelViewSet):
    """
        URL: licensee/pk:int
        Method: Put, Get(Retrieve), Delete
        Put Method:
            data: {
                phone_number: str,
                nmls_number: str,
                dre_license: str,
                ref_code: str
            }

            Returns Saved Data

        Retrieve Method:
            Returns Referred Data

        Delete Method:
            Deletes Referred Account and data

        """
    model = Referred
    serializer_class = ReferredSerializer
    lookup_url_kwarg = "pk"
    lookup_field = "id"
    queryset = Referred.objects.get_queryset()
