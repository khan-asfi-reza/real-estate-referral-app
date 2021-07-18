from django.db import models
from django.contrib.auth import get_user_model

from Core.models.managers import RecruiterModelManager

User = get_user_model()


# Referrer Model
class Recruiter(models.Model):
    # Referrer User
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, limit_choices_to={"role": 1})
    # Unique Ref code
    ref_code = models.CharField(max_length=24, unique=True, null=True, blank=True)

    def __str__(self):
        return self.user.email

    @property
    def username(self):
        return self.user.email

    objects = RecruiterModelManager()


