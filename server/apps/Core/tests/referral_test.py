import logging

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from server.apps.Account.tests.test_utils import create_unique_test_user
from server.apps.Core.models import Referral
from server.apps.Core.tests.utils import create_unique_test_recruiter


class ReferralTest(APITestCase):

    def test_referral(self):
        # Request User
        req_user_data, req_user = create_unique_test_user(1)

        # recruit User
        ref_user_1_data, ref_user_1 = create_unique_test_user(2)
        ref_user_2_data, ref_user_2 = create_unique_test_user(2)

        # Bulk Create
        Referral.objects.bulk_create([
            Referral(recruiter=req_user, recruit=ref_user_1),
            Referral(recruiter=req_user, recruit=ref_user_2),
        ])

        # Test
        token, created = Token.objects.get_or_create(user=req_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        res = self.client.get(reverse("referral-list"),
                              headers={"authorization": Token.objects.get_or_create(user=req_user)[0]})
        if res.status_code == 400:
            logging.Logger(__name__).error(res.data)

        self.assertEqual(res.status_code, 200)

    def test_ref_code(self):
        # Get Recruiter
        user_data, rec = create_unique_test_recruiter()
        # Test Recruiter
        self.assertEqual(rec.user.email, user_data["email"])
        # URL
        url = reverse("ref-code")
        # Client Post
        res = self.client.post(url, {"ref_code": rec.ref_code})
        # Test
        self.assertEqual(res.status_code, 200)
