import sys

from django.urls import reverse
from rest_framework.test import APITestCase
import logging
from Account.models import ForgetPassword
from Account.tests.test_utils import get_unique_user_data
from Core.models import Transaction
from Core.const import TRANSACTION_PROFIT_RATE, TRANSACTION_PROFIT
from Core.models.transaction import Commission, CommissionPayment
from ShoreCapitalReferral.env import TEST_EMAIL


class IntegrationTest(APITestCase):

    def login(self, credentials):
        login_url = reverse("login")
        res = self.client.post(login_url, {"email": credentials["email"],
                                           "password": credentials["password"]})
        self.assertEqual(res.status_code, 200)
        return res.data["token"]

    def test_integration(self):
        sys.stdout.write("\nIntegration Testing")
        sys.stdout.write("-"*10,)
        sys.stdout.write("\n")
        # Recruiter and Recruit Data
        recruiter_data = get_unique_user_data()
        recruit_data = get_unique_user_data(2)

        # Set Recruiter Email
        if TEST_EMAIL:
            recruiter_data["email"] = TEST_EMAIL

        # Part 1 - Create Recruit Data
        recruiter_create_url = reverse("recruiter-create")
        res = self.client.post(recruiter_create_url, {"user": recruiter_data}, format="json")
        self.assertEqual(res.status_code, 201)
        sys.stdout.write(f"\n1. Create Recruiter -  ✔")

        # Part 2 - Recruiter Login
        token = self.login(recruiter_data)
        sys.stdout.write(f"\n2. Login Recruiter -  ✔")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        # Part 3 Get Ref Code
        ref_code_url = reverse("recruiter-crud")
        res = self.client.get(ref_code_url)
        self.assertEqual(res.status_code, 200)
        ref_code = res.data["ref_code"]
        sys.stdout.write(f"\n3. Ref Code Getter -  ✔")

        # Part 4 Register Recruit
        register_recruit_url = reverse("recruit-create-list")
        self.client.credentials(HTTP_AUTHORIZATION="")
        res = self.client.post(register_recruit_url,
                               {
                                   "user": recruit_data,
                                   "ref_code": ref_code,
                                   "nmls_number": "NMLS NUMBER",
                                   "dre_license": "DRE LICENSE",
                                   "cba_licence": True,
                                   "association": "ASSOCIATION"
                               },
                               format="json"
                               )
        self.assertEqual(res.status_code, 201)
        recruit_id = res.data["data"]["user"]["id"]

        sys.stdout.write(f"\n4. Recruit Register -  ✔")

        # Part 5 - Get Info
        token = self.login(recruiter_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        recruiter_info_url = reverse("recruiter-info")
        res = self.client.get(recruiter_info_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["total_recruited"], 1)
        self.assertEqual(res.data["bonus"], 0)
        sys.stdout.write("\n5. Bonus Recruiter Info Data - ✔")

        # Part 6 - Get Referral
        referral_url = reverse("referral-list")
        res = self.client.get(referral_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)
        sys.stdout.write("\n6. Referral List - ✔")

        # Part 7 - Transaction & Profit Check
        AMOUNT = 5000
        transaction = Transaction.objects.create(recruit_id=recruit_id, amount=AMOUNT)
        estimated_bonus = TRANSACTION_PROFIT
        res = self.client.get(recruiter_info_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["total_recruited"], 1)
        self.assertEqual(res.data["bonus"], estimated_bonus)
        sys.stdout.write("\n7. Transaction & Profit Check - ✔")

        # Part 8 - Transaction Commission Check
        com = Commission.objects.get(recruit_id=recruit_id)
        self.assertEqual(com.commission, estimated_bonus)
        sys.stdout.write("\n8. Commission & Profit Check - ✔")

        # Part 9 - Forget Password
        fp_api = reverse("forget-password")
        res = self.client.post(fp_api, {"email": recruiter_data["email"]}, format="json")
        self.assertEqual(res.status_code, 201)
        sys.stdout.write("\n9. Password Change Request Check - ✔")

        # part 10 - Validate Password Unique Link
        reset_link = ForgetPassword.objects.get(user__email=recruiter_data["email"])
        validation_api = reverse("validate-reset-link")
        res = self.client.post(validation_api, {"unique_link": reset_link.unique_link}, format="json")
        self.assertEqual(res.status_code, 200)
        sys.stdout.write("\n10. Password Reset Link Check - ✔")

        # Part 11 - Reset Password
        reset_api = reverse("reset-password")
        res = self.client.post(reset_api, {"email": recruiter_data["email"],
                                           "unique_link": reset_link.unique_link,
                                           "password": "NEW_PASSWORD_TEST_2020"})
        self.assertEqual(res.status_code, 201)
        sys.stdout.write("\n11. Password Reset Check - ✔")

        # Part 12 - Test Transaction Payment
        cp = CommissionPayment.objects.create(commission=com, amount=50, )
        self.assertEqual(com.paid_commission, cp.amount)
        sys.stdout.write("\n12. Transaction Payment Check - ✔\n")