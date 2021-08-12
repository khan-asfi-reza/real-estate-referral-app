from datetime import timedelta

from django.utils import timezone


def get_expiration_time():
    return timezone.now() + timedelta(hours=1)
