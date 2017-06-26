from django.core.exceptions import ValidationError

from trymake.apps.customer.models import Customer


def validator_email_doesnt_exist(email):
    if Customer.objects.filter(email=email).exists():
        raise ValidationError("Email is already in use", code="email_exists")