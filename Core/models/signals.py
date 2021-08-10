import logging
import sys

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from Core.const import TRANSACTION_PROFIT_BASE_AMOUNT, TRANSACTION_PROFIT
from Core.models.transaction import Transaction, Commission, CommissionPayment
from Core.models.referral import Referral
from Core.models.recruiter import Recruiter

# Create Unique Ref Code after recruiter creation
from Core.send_email import SendEmail


@receiver(post_save, sender=Recruiter, dispatch_uid="Recruiter_REF_CODE_CREATE")
def recruiter_post_create(sender, instance, created, *args, **kwargs):
    # If the object is created
    if created:
        # Generate random String
        instance.ref_code = get_random_string(20)
        instance.save()


# Creates Commission After Transaction
@receiver(post_save, sender=Transaction, dispatch_uid="Transaction Post Save Commission Creation")
def transaction_post_save(sender, instance, created, *args, **kwargs):
    # If the object is created
    if created:
        # Check if amount is more than permissible amount
        if instance.amount >= TRANSACTION_PROFIT_BASE_AMOUNT:
            try:
                # Get Referral Relationship
                ref = Referral.objects.get(recruit=instance.recruit)
                # Check Valid Relationship
                if ref.recruiter is not None:
                    # Commission Model Create
                    commission = Commission.objects.create(recruit=instance.recruit,
                                                           transaction=instance,
                                                           recruiter=ref.recruiter,
                                                           )
                    # Set Transaction
                    commission.commission = TRANSACTION_PROFIT
                    # Save Transaction
                    commission.save()
            # Throw Error If Invalid Referral
            except Referral.DoesNotExist:
                logging.error("Invalid Referral and Recruit")


# Commission Payment Post Save
@receiver(post_save, sender=CommissionPayment, dispatch_uid="Commission Payment Post Save")
def commission_payment_post_save(sender, instance, created, *args, **kwargs):
    # If Object is created
    if created:
        # Send Email Notification
        instance.commission.all().update(completed=True)
        SendEmail.send_custom_context_html_email(template="commission_transaction.html",
                                                 subject="A Commission Transaction has been made",
                                                 context={
                                                     "trxid": instance.id,
                                                     "amount": instance.amount,
                                                     "date": instance.time_stamp
                                                 },
                                                 to=instance.recruiter.email
                                                 )
