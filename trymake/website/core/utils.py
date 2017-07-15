"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
from django.template import Template
from django.template.loader import get_template

from trymake.apps.SMS_manager import MessageSender, SMS
from trymake.apps.customer.models import Customer, UniqueToken, EMAIL_VERIFICATION, EMAIL_PASSWORD_RESET

sms_sender = MessageSender()


def send_OTP(phone, otp):
    message = "Your Trymake One Time Password is {0}".format(otp)
    sms_sender.send_sms(SMS(phone_number=phone, message=message))


def generate_token(customer: Customer, type: int) -> str:
    token = UniqueToken.create_token(customer.id, type)
    return token


def send_verification_email(customer: Customer) -> None:
    verification_token = generate_token(customer, UniqueToken.EMAIL_VERIFICATION_TOKEN)  # type: str
    customer.send_template_mail(EMAIL_VERIFICATION, context={'token': verification_token})


def send_password_reset_email(customer: Customer) -> None:
    verification_token = generate_token(customer, UniqueToken.PASSWORD_RESET_TOKEN)  # type: str
    customer.send_template_mail(EMAIL_PASSWORD_RESET, context={'token': verification_token})


def get_customer(id=None, email=None, user=None):
    try:
        if id is not None:
            return Customer.objects.get(id=id)
        if email is not None:
            return Customer.objects.get(email=email)
        if user is not None:
            return Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return None
    raise KeyError("No valid key found")
