import logging
import django.db.models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from Core.const import TRANSACTION_PROFIT_BASE_AMOUNT, TRANSACTION_PROFIT
from Core.models.transaction import Transaction, Commission, CommissionTransaction
from Core.models.referral import Referral
from Core.models.recruiter import Recruiter
from Core.send_email import SendEmail
# Create Unique Ref Code after recruiter creation


@receiver(post_save, sender=Recruiter, dispatch_uid="Recruiter_REF_CODE_CREATE")
def recruiter_post_create(sender: django.db.models.Model, instance: Recruiter, created: bool, *args: tuple, **kwargs: dict):
    # If the object is created
    if created:
        # Generate random String
        instance.ref_code = get_random_string(20)
        instance.save()


# Creates Commission After Transaction
@receiver(post_save, sender=Transaction, dispatch_uid="Transaction Post Save Commission Creation")
def transaction_post_save(sender: django.db.models.Model, instance: Transaction, created: bool, *args: tuple, **kwargs: dict):
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
@receiver(post_save, sender=CommissionTransaction, dispatch_uid="Commission Payment Post Save")
def commission_payment_post_save(sender: django.db.models.Model, instance: CommissionTransaction, created, *args, **kwargs):
    # If Object is created
    if created:
        # Send Email Notification
        # Set To CommissionPayment
        instance.amount = instance.commission_amount_total if not instance.amount else instance.amount
        # If instance commission object list is empty
        instance.commission.add(*instance.commission_object_query)
        # Update Commission Intents To Complete
        instance.update_commission_complete()
        # Save Instance
        instance.save()
        # Send Email
        SendEmail.send_custom_context_html_email(template="commission_transaction.html",
                                                 subject="A Commission Transaction has been made",
                                                 context={
                                                     "trxid": instance.id,
                                                     "amount": instance.amount,
                                                     "date": instance.time_stamp
                                                 },
                                                 to=instance.recruiter.email
                                                 )
