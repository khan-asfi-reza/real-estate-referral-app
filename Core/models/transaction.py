import logging
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from Core.const import TRANSACTION_PROFIT_BASE_AMOUNT, TRANSACTION_PROFIT

User = get_user_model()


# Transaction
class Transaction(models.Model):
    # Recruit Who Completed Transaction
    recruit = models.ForeignKey(to=User, on_delete=models.CASCADE, limit_choices_to={'role': 2})
    # Amount Completed
    amount = models.FloatField()
    # Time when completed
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recruit.email


# Commission
class Commission(models.Model):
    # Recruiter Who Recruited The Recruit
    recruiter = models.ForeignKey(to=User,
                                  related_name="referral_recruiter",
                                  on_delete=models.CASCADE,
                                  limit_choices_to={'role': 1})
    # Recruit
    recruit = models.ForeignKey(to=User,
                                related_name="commission_recruit",
                                on_delete=models.SET_NULL,
                                null=True,
                                limit_choices_to={'role': 2})
    # Commission Amount
    commission = models.FloatField(default=0.0)
    # Transaction ID
    transaction = models.OneToOneField(to=Transaction, on_delete=models.CASCADE)
    # When Was Completed
    time_stamp = models.DateTimeField(auto_now_add=True)
    # Did The recruiter get the bonus
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.time_stamp} - {self.recruiter.email}"


# Creates Commission After Transaction
@receiver(post_save, sender=Transaction, dispatch_uid="Transaction Post Save Commission Creation")
def recruiter_post_create(sender, instance, created, *args, **kwargs):
    from .referral import Referral
    if created:
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
                    commission.commission = TRANSACTION_PROFIT
                    commission.save()
            except Referral.DoesNotExist:
                logging.error("Invalid Referral and Recruit")
