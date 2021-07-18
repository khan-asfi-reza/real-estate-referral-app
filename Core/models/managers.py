from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class RecruiterModelManager(models.Manager):

    def get_recruiter(self, ref_code):
        try:
            return self.get(ref_code=ref_code).user
        except ObjectDoesNotExist:
            return None


