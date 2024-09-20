from userauth.models import User
from django.utils.crypto import get_random_string
from userauth.models import User


def send_verification_link(email):
    try:
        user = User.objects.get(email=email)
        verification_code = get_random_string(length=35).lower()

        return verification_code
    except User.DoesNotExist:
        return False
    except Exception as e:
        return False
