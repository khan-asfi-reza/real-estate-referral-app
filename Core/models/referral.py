from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Referral(models.Model):
    # The user who referred another user
    recruiter = models.ForeignKey(to=User,
                                  related_name="recruiter_user",
                                  null=True,
                                  on_delete=models.SET_NULL,
                                  limit_choices_to={'role': 1})
    # The user who is being referred
    recruit = models.OneToOneField(to=User,
                                   related_name="recruit_user",
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   limit_choices_to={'role': 2})
    # Time of Creation
    time_stamp = models.DateTimeField(auto_now_add=True)
    # Time of update
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["recruiter", "recruit"]

    def __str__(self):
        return f"{self.id} - {self.time_stamp}"
