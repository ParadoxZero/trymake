"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
from django.template import Template
from django.template.loader import get_template

from trymake.apps.customer.models import Customer, EmailVerificationToken, EMAIL_VERIFICATION


def generate_verification_token(customer: Customer) -> str:
    token = EmailVerificationToken.create_token(customer.id)
    return token


def send_verification_email(customer: Customer) -> None:
    verification_token = generate_verification_token(customer)  # type: str
    customer.send_template_mail(EMAIL_VERIFICATION, context={'token': verification_token})

