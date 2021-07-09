from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import Q
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USStateField

from Account.utils import get_expiration_time


class UserManager(BaseUserManager):

    # Create User Method
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

    # Create Normal User
    def create_user(self, email, password, role, *args, **kwargs):
        return self.__create_user(email, password, role, *args, **kwargs)

    # Create Admin Users
    def create_superuser(self, email, password, role, *args, **kwargs):
        return self.__create_user(email, password, role, *args, **kwargs,
                                  is_staff=True,
                                  is_active=True,
                                  is_superuser=True, )

    def create_staff(self, email, password, role, *args, **kwargs):
        return self.__create_user(email, password, role, *args, **kwargs,
                                  is_staff=True,
                                  is_active=True,
                                  is_superuser=False, )

    # Returns Admin Staff Users
    def get_admin_staff_users(self):
        return self.filter(Q(is_staff=True) | Q(is_superuser=True))


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


class AdminUser(User):
    class Meta:
        proxy = True
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"


# Forget Email
class ForgetPassword(models.Model):
    REQUEST_SENT_THRESHOLD = 6
    # User
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    # Unique Link
    unique_link = models.CharField(max_length=30, blank=True, null=True)
    # Creation Time
    time_stamp = models.DateTimeField(auto_now_add=True)
    # Expiration Time
    expiration_time = models.DateTimeField(default=get_expiration_time)
    # Changed
    changed = models.BooleanField(default=False)
    # Request Sent
    request_sent = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.user.email}"
