from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USStateField


class UserManager(BaseUserManager):

    def __create_user(self, email, password, role, *args, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            role=role,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, role, *args, **kwargs):
        return self.__create_user(email, password, role, *args, **kwargs)

    def create_superuser(self, email, password, role, *args, **kwargs):
        return self.__create_user(email, password, role, *args, **kwargs,
                                  is_staff=True,
                                  is_active=True,
                                  is_superuser=True, )


class User(AbstractUser):
    email = models.EmailField(unique=True)
    # User Phone Number
    phone_number = models.CharField(null=True, blank=True, max_length=20)
    # User Role
    role = models.PositiveSmallIntegerField(choices=[(1, "Recruiter"), (2, "Recruit"), (3, "Admin")])
    # User Address
    address = models.TextField(blank=True, null=True)
    # City Name
    city = models.CharField(max_length=50, blank=True, null=True)
    # US STATES
    state = USStateField(choices=STATE_CHOICES, blank=True, null=True)
    # Zip Code
    zip = models.CharField(max_length=33, blank=True, null=True)
    # Username
    username = None

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["role"]

    objects = UserManager()

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
