from django.test import TestCase
from server.apps.Account.tests import create_unique_test_user
from server.apps.Core.models import Referral, Transaction
from server.apps.Core.const import TRANSACTION_PROFIT
from server.apps.Core.models.transaction import Commission


class TransactionTest(TestCase):

    def test_transaction(self):
        # Test Amount
        test_amount = 5000
        # Create Test Recruiter and Recruit
        recruiter_data, recruiter = create_unique_test_user(1)
        user_data, recruit = create_unique_test_user(2)
        # Create Referral
        Referral.objects.create(recruiter=recruiter, recruit=recruit)
        # Create Transaction
        Transaction.objects.create(recruit=recruit, amount=test_amount)
        # Check Commission
        com = Commission.objects.get(recruiter=recruiter, recruit=recruit)
        self.assertEqual(com.commission, TRANSACTION_PROFIT)


