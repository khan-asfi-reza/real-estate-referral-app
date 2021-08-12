import random
import time
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

DEF_TEST_PASSWORD = "Password1234@"

User = get_user_model()


# Role ==> 1: Recruiter 2: Referred User
def get_user_data(role: int = 1):
    return {
        "phone_number": "+9901231231",
        "email": "test_user@gmail.com",
        "password": DEF_TEST_PASSWORD,
        "role": role,
        "address": "TEST ADDRESS",
        "city": "TEST CITY",
        "state": "AL",
        "zip": "2020"
    }


def get_unique_user_data(role=1):
    return {
        "phone_number": "+12312312366",
        "email": f"EMAIL{random.randrange(1000000)+random.randrange(999)}@email.com",
        "password": DEF_TEST_PASSWORD,
        "role": role,
        "address": "TEST ADDRESS",
        "city": "TEST CITY",
        "state": "AL",
        "zip": "2020"
    }


def create_test_user(role=1):
    # Test User
    # Create user
    user_data = get_user_data(role)
    user = User.objects.create(**user_data)
    # Set password
    user.set_password(user_data["password"])
    # Save
    user.save()
    return user


def create_unique_test_user(role=1):
    user_data = get_unique_user_data()
    user = User.objects.create(**user_data)
    user.set_password(user_data["password"])
    user.save()
    return user_data, user


def get_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token