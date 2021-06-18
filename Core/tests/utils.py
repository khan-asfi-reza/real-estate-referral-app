from Account.tests.test_utils import create_test_user, create_unique_test_user
from Core.models import Recruiter


def create_test_recruiter():
    # Create Referrer Account
    recruiter = Recruiter(
        user=create_test_user(1),
    )
    # Save Referrer
    recruiter.save()
    return recruiter


def create_unique_test_recruiter():
    user_data, user = create_unique_test_user(1)

    recruiter = Recruiter(
        user=user
    )

    recruiter.save()

    return user_data, recruiter