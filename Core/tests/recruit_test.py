import json

from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from Core.models import Recruit, Referral
from django.contrib.auth import get_user_model
import logging
from Core.tests.utils import create_test_recruiter
from Account.tests.test_utils import get_user_data, get_unique_user_data
from Core.views.recruit import RecruitUserCRUDApi, RecruitUserCreateListApi

User = get_user_model()
logger = logging.getLogger(__name__)


class RecruitTest(APITestCase):
    recruit_data = {
        "nmls_number": "123456",
        "dre_license": "123455",
    }

    def create_test_recruit(self):
        # Test User
        # Create user
        user_data = get_user_data(2)
        user = User.objects.create(**user_data)
        # Set password
        user.set_password("Password1234@")
        # Save
        user.save()
        # Test
        self.assertEqual(user.email, user_data["email"])
        # Create Referrer Account
        recruit = Recruit(
            user=user,
            nmls_number=self.recruit_data["nmls_number"],
            dre_license=self.recruit_data["dre_license"],
        )
        # Save Referrer
        recruit.save()
        return recruit

    def test_url(self):
        # Create API Url Test
        create_url = resolve(reverse("recruit-create-list"))
        self.assertEqual(create_url.func.__name__, RecruitUserCreateListApi.as_view().__name__)
        # CRUD Api Url Test
        crud_url = resolve(reverse("recruit-crud", kwargs={"pk": 1}))
        self.assertEqual(crud_url.func.__name__, RecruitUserCRUDApi.as_view({
            "put": "partial_update",
            "get": "retrieve",
            "delete": "destroy"
        }).__name__)

    def test_recruit_model_create(self):
        recruit = self.create_test_recruit()
        # Test
        self.assertEqual(recruit.nmls_number, self.recruit_data["nmls_number"])
        self.assertEqual(recruit.dre_license, self.recruit_data["dre_license"])

    def test_recruit_create_api(self):
        # Referrer
        referrer = create_test_recruiter()
        # Test User Creation
        user = get_unique_user_data(2)
        res = self.client.post(
            reverse("recruit-create-list"),
            {
                "user": user,
                "nmls_number": self.recruit_data["nmls_number"],
                "dre_license": self.recruit_data["dre_license"],
                "ref_code": referrer.ref_code
            },
            format='json'
        )

        referral = Referral.objects.filter(recruit_id=res.data["data"]["user"]["id"], recruiter=referrer.user)
        self.assertEqual(referral.count(), 1)
        self.assertEqual(res.status_code, 201)

        # Test Duplicate Account
        res_dup = self.client.post(
            reverse("recruit-create-list"),
            {
                "user": user,
                "nmls_number": self.recruit_data["nmls_number"],
                "dre_license": self.recruit_data["dre_license"],
            },
            format='json')

        # Check if exists
        self.assertEqual(res_dup.status_code, 400)

    def test_list_api(self):
        res = self.client.get(reverse("recruit-create-list"))
        self.assertEqual(res.status_code, 200)

    def test_update_delete_api(self):
        # Partial Update
        recruit = self.create_test_recruit()
        # Get Test
        res = self.client.get(reverse("recruit-crud", kwargs={"pk": recruit.id}))
        self.assertEqual(res.status_code, 200)
        # Update Test
        res = self.client.put(
            reverse("recruit-crud",
                    kwargs={"pk": recruit.id}),
            {
                "nmls_number": "NEW_UPDATED_NMLS_NUMBER",
            },
            format="json")
        self.assertEqual(res.status_code, 200)
        # Delete
        res = self.client.delete(reverse("recruit-crud", kwargs={"pk": recruit.id}))
        self.assertEqual(res.status_code, 204)
