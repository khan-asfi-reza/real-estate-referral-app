import logging
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from Core.models import Recruiter
from Core.tests.utils import create_test_recruiter, create_unique_test_recruiter
from Account.tests.test_utils import get_user_data, create_unique_test_user, get_unique_user_data
from Core.views.recruiter import RecruiterCreateApi

User = get_user_model()
logger = logging.getLogger(__name__)


class RecruiterTest(APITestCase):
    # Test URL
    def test_url(self):
        recruiter_create_url = resolve(reverse("recruiter-create"))
        self.assertEqual(recruiter_create_url.func.__name__, RecruiterCreateApi.as_view().__name__)

    # Test MODEL
    def test_recruiter_model_create(self):
        user_data = get_user_data(1)
        recruiter = create_test_recruiter()
        self.assertEqual(recruiter.user.email, user_data["email"])

    # Test Api
    def test_recruiter_api(self):
        # Test User Creation
        user = get_user_data(1)
        res = self.client.post(
            reverse("recruiter-create"),
            {
                "user": user,
            },
            format='json'
        )
        # Test User with Refer Account
        self.assertEqual(res.status_code, 201)

        # Check user
        self.assertEqual(res.data["data"]["user"]["email"], user["email"])
        self.assertEqual(res.data["data"]["user"]["state"], user["state"])
        self.assertEqual(res.data["data"]["user"]["address"], user["address"])
        self.assertEqual(res.data["data"]["user"]["zip"], user["zip"])
        self.assertEqual(res.data["data"]["user"]["city"], user["city"])
        self.assertEqual(res.data["data"]["user"]["role"], user["role"])
        # Test Duplicate Account
        res_dup = self.client.post(
            reverse("recruiter-create"),
            {
                "user": user,
                "billing_address": "NEW BILLING ADDRESS",
            },
            format='json')

        # Check if exists
        self.assertEqual(res_dup.status_code, 400)

    def test_recruiter_crud(self):
        # URL
        url = reverse("recruiter-crud")
        # Generate unique user
        user_data, user = create_unique_test_user(role=1)
        # Create Recruiter
        rec = Recruiter.objects.create(user=user)
        # Check user and recruiter
        self.assertEqual(rec.user.email, user_data["email"])
        # Login client
        self.client.login(email=user_data["email"], password=user_data["password"])
        # Get Token
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        # Send response
        res = self.client.get(url)
        # Test Status code
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["ref_code"], rec.ref_code)

    def test_ref_code(self):
        # Create Recruiter
        user_data, user = create_unique_test_user()
        recruiter = Recruiter.objects.create(user=user)
        # url
        url = reverse("ref-code")
        # Client Get
        res = self.client.post(url, {
            "ref_code": recruiter.ref_code
        })
        # Test
        self.assertEqual(res.status_code, 200)

    def test_recruiter_all_info(self):
        # Unique Users
        unique_users = [get_unique_user_data(2) for i in range(5)]
        # Unique Recruiter
        user_data, recruiter = create_unique_test_recruiter()
        # URL
        recruit_create_url = reverse("recruit-create-list")
        # Create Test users
        for i, user in enumerate(unique_users):
            self.client.post(recruit_create_url, {
                "user": user,
                "dre_license": f"TEST_LICENSE_{i}",
                "nmls_number": f"TEST_NMLS_{i}",
                "cba_license": i % 2 == 0,
                "association": "TEST_ASSOCIATION",
                "ref_code": recruiter.ref_code
            }, format="json")

        # Get Token
        token, created = Token.objects.get_or_create(user=recruiter.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        # Recruiter Info URL
        recruiter_info_url = reverse("recruiter-info", )
        res = self.client.get(recruiter_info_url)
        self.assertEqual(res.status_code, 200)