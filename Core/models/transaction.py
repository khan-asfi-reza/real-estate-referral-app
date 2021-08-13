from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum


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

    def __str__(self):
        return f"{self.recruiter.email} - {self.id} - {self.time_stamp.strftime('%Y:%m:%d')}"


# Paid Commission Amounts
class CommissionTransaction(models.Model):
    recruiter = models.ForeignKey(to=User,
                                  related_name="commission_transaction_owner",
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  limit_choices_to={'role': 1},
                                  )
    # Commission
    commission = models.ManyToManyField(to=Commission,
                                        limit_choices_to={"completed": False},
                                        blank=True
                                        )
    # Amount
    amount = models.FloatField(default=0.0)
    # When Was Create
    time_stamp = models.DateTimeField(auto_now_add=True)
    # Updated
    updated = models.DateTimeField(auto_now=True)

    # Returns All Commission Objects
    @property
    def commission_object_query(self):
        return Commission.objects.filter(recruiter=self.recruiter, completed=False)

    # Returns Total Commission Amount
    @property
    def commission_amount_total(self):
        data = self.commission_object_query.aggregate(Sum('commission'))
        return data["commission__sum"]

    # Update all incomplete commissions
    def update_commission_complete(self):
        self.commission.all().update(completed=True)

    # Clean Method raise validation if amount is more than the summation of all commissions
    def clean(self):
        if self.amount > self.commission_amount_total:
            raise ValidationError(
                {
                    "amount": "Max Threshold exceeded"
                }
            )

        if self.recruiter is None:
            raise ValidationError({
                "recruiter": "Recruiter cannot be empty"
            })

    class Meta:
        verbose_name = "Commission Transaction"
        verbose_name_plural = "Commission Transactions"
