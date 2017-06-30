"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from trymake.apps.customer.models import Customer

phone_validator = RegexValidator(regex=r"[0-9]{10}", message="Format: 9999999999")
pin_validator = RegexValidator(regex=r"[0-9]{6}", message="Format: 999999")


def email_doesnt_exist(email):
    if Customer.objects.filter(email=email).exists():
        raise ValidationError("Email is already in use", code="email_exists")


def phone_doesnt_exist(phone):
    if Customer.objects.filter(phone=phone).exists():
        raise ValidationError("Phone number already in use", code="phone_exists")
