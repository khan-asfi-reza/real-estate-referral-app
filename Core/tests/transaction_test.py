import logging
from django.test import TestCase
from Account.tests import create_unique_test_user
from Core.models import Referral, Transaction
from Core.const import TRANSACTION_PROFIT_RATE
from Core.tests.utils import create_unique_test_recruiter


class TransactionTest(TestCase):

    def test_transaction(self):
        test_amount = 5000
        recruiter_data, recruiter = create_unique_test_user(1)
        user_data, recruit = create_unique_test_user(2)
        Referral.objects.create(recruiter=recruiter, recruit=recruit)
        Transaction.objects.create(recruit=recruit, amount=test_amount)
        ref = Referral.objects.get(recruiter=recruiter, recruit=recruit)
        self.assertEqual(ref.commission, test_amount*TRANSACTION_PROFIT_RATE)


