import json
import logging

from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Create your tests here.
from Account.models import User
from Account.tests.test_utils import create_unique_test_user, DEF_TEST_PASSWORD, get_token

logger = logging.Logger(__name__)


class LoginUserTest(APITestCase):

    def test_user_login(self):
        # User Data
        user_data, user = create_unique_test_user(1)
        # Check User
        self.assertEqual(user.email, user_data["email"])
        # Login URL
        url = reverse("login")

        res = self.client.post(url, {
            "email": user_data["email"],
            "password": user_data["password"]
        })

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.data['token'])

    def test_user(self):
        # User data
        user_data, user = create_unique_test_user(2)
        # Check user
        self.assertEqual(user.email, user_data["email"])
        self.assertEqual(user.state, user_data["state"])
        self.assertEqual(user.address, user_data["address"])
        self.assertEqual(user.zip, user_data["zip"])
        self.assertEqual(user.city, user_data["city"])
        self.assertEqual(user.role, user_data["role"])

    def test_super_user(self):
        user = User.objects.create_superuser(
            email="TESTADMIN@gmail.com",
            role=1,
            password="PASSWORD20",
        )
        self.assertEqual(user.email, "TESTADMIN@gmail.com")
        self.assertEqual(user.is_superuser, True)

    def test_user_change_password(self):
        user_data, user = create_unique_test_user(1)
        url = reverse("change-password")
        token, created = Token.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        res = self.client.post(url, {
            "old_password": DEF_TEST_PASSWORD,
            "new_password": "NEW_TEST_PASSWORD@12"
        }, format="json")
        self.assertEqual(res.status_code, 201)

    def test_user_change_password_2(self):
        user_data, user_2 = create_unique_test_user(2)
        url = reverse("change-password")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {get_token(user_2)}")
        res = self.client.post(url, {
            "old_password": DEF_TEST_PASSWORD,
            "new_password": "NEW_TEST_PASSWORD@12"
        }, format="json")
        self.assertEqual(res.status_code, 201)

    def test_user_update(self):
        user_data, user = create_unique_test_user(1)
        url = reverse("user-update")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {get_token(user)}")
        res = self.client.patch(url, {
            "address": "MY NEW ADDRESS",
            "phone_number": "MY NEW PHONE NUMBER"
        }, format="json")

        self.assertEqual(200, res.status_code)

    def test_email_exist(self):
        user_data, user = create_unique_test_user(1)
        url = reverse("email-check")
        res = self.client.post(url, {"email": "userTest1234@testemail.com"}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["msg"], 1)

        res = self.client.post(url, {"email": user_data["email"]}, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["msg"], 0)

    def test_forget_password(self):
        data, user = create_unique_test_user(1)

        url = reverse("forget-password")
        # Post Request 4 times
        for i in range(5):
            res = self.client.post(url, {"email": user.email}, format="json")
            self.assertEqual(res.status_code, 201)
            self.assertEqual(res.data["msg"], 1)

        # Error
        res = self.client.post(url, {"email": user.email}, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data["msg"], 0)
