from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


# Referred Model
class Recruit(models.Model):
    # Referred User
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="recruit", limit_choices_to={"role": 2})
    # Department of real estate License
    dre_license = models.CharField(max_length=100, null=True, blank=True)
    # NMLS License Number
    nmls_number = models.CharField(max_length=100, null=True, blank=True)
    # CBA License
    cba_licence = models.BooleanField(default=False)
    # Association
    association = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.email

    @property
    def username(self):
        return self.user.email
