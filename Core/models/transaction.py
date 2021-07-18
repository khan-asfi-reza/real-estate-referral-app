from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

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
        return f"{self.id}"


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
    # When Was Create
    time_stamp = models.DateTimeField(auto_now_add=True)
    # Updated
    updated = models.DateTimeField(auto_now=True)
    # Did The recruiter get the bonus
    completed = models.BooleanField(default=False)
    # Paid Amount
    paid_commission = models.FloatField(default=0.0, )

    def __str__(self):
        return f"{self.id} - {self.time_stamp} - {self.recruiter.id}"


# Paid Commission Amounts
class CommissionPayment(models.Model):
    # Transaction ID
    transaction_id = models.PositiveBigIntegerField(blank=True)
    # Commission
    commission = models.ForeignKey(to=Commission, on_delete=models.CASCADE)
    # Amount
    amount = models.FloatField(default=0.0)
    # When Was Create
    time_stamp = models.DateTimeField(auto_now_add=True)
    # Updated
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        # If Commission Payment Passes the commission amount threshold
        if self.commission.paid_commission + self.amount > self.commission.commission:
            raise ValidationError({
                'paid': 'Amount exceeded',
                'commission': 'Cannot save commission'
            })

        self.transaction_id = self.commission.transaction.id

    def save(self, *args, **kwargs):
        # If Transaction Id is invalid
        if not self.transaction_id:
            self.transaction_id = self.commission.transaction.id
        super(CommissionPayment, self).save(*args, **kwargs)
