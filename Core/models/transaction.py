import logging
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .const import TRANSACTION_PROFIT_BASE_AMOUNT, TRANSACTION_PROFIT_RATE

User = get_user_model()


class Transaction(models.Model):
    recruit = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount = models.FloatField()
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recruit.email


@receiver(post_save, sender=Transaction, dispatch_uid="Transaction Post Save")
def recruiter_post_create(sender, instance, created, *args, **kwargs):
    from .referral import Referral
    if created:
        if instance.amount >= TRANSACTION_PROFIT_BASE_AMOUNT:
            try:
                ref = Referral.objects.get(recruit=instance.recruit)
                ref.commission = instance.amount * TRANSACTION_PROFIT_RATE
                ref.save()
            except Referral.DoesNotExist:
                logging.error("Invalid Referral and Recruit")
