from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save

User = get_user_model()


class RecruiterModelManager(models.Manager):

    def get_recruiter(self, ref_code):
        try:
            return self.get(ref_code=ref_code).user
        except ObjectDoesNotExist:
            return None


# Referrer Model
class Recruiter(models.Model):
    # Referrer User
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    # Unique Ref code
    ref_code = models.CharField(max_length=24, unique=True, null=True, blank=True)

    def __str__(self):
        return self.user.email

    @property
    def username(self):
        return self.user.email

    objects = RecruiterModelManager()


@receiver(post_save, sender=Recruiter, dispatch_uid="Recruiter_REF_CODE_CREATE")
def recruiter_post_create(sender, instance, created, *args, **kwargs):
    if created:
        instance.ref_code = get_random_string(20)
        instance.save()
