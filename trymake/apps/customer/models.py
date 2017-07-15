"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

import uuid

import pyotp
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import IntegrityError
from django.db import models
from django.db.models import QuerySet
from django.template import Template
from django.template.loader import get_template
from django.utils import timezone

from trymake.apps.validators import phone_validator, pin_validator


class EmailTemplate:
    def __init__(self, template, subject, from_mail='no-reply@notifications.trymake.com'):
        self.template = get_template(template)  # type: Template
        self.subject = subject
        self.from_mail = from_mail


EMAIL_VERIFICATION = 'email_verification'
EMAIL_VERIFIED = 'email_verified'
EMAIL_PASSWORD_RESET = 'password_reset'
EMAIL_WELCOME = 'welcome'
EMAIL_TEMPLATES = {
    EMAIL_VERIFICATION: EmailTemplate(template='website/emails/verification.html',
                                      subject="Please verify your email"),
    EMAIL_VERIFIED: EmailTemplate(template='website/emails/verified.html',
                                  subject="Thank you for verifying you email"),
    EMAIL_PASSWORD_RESET: EmailTemplate(template="website/emails/password_reset.html",
                                        subject="Link to reset your Trymake password"),
    EMAIL_WELCOME: EmailTemplate(template="website/emails/welcome.html",
                                 subject="Welcome to Trymake")
}


class Customer(models.Model):
    GROUP_NAME = "Customer"
    PASSWORD_RESET_CUSTOMER = 'password_reset_customer'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.OneToOneField(User, unique=True)
    email = models.EmailField(unique=True, null=False, db_index=True)
    name = models.CharField(max_length=250)
    is_verified = models.BooleanField(default=False)

    phone_validator = RegexValidator(regex=r"[0-9]{10}", message="Format: 9999999999")
    phone = models.CharField(validators=[phone_validator], max_length=11, unique=True)
    phone_verified = models.BooleanField(default=False)

    default_address = models.ForeignKey('Address', null=True, on_delete=models.SET_NULL, related_name='default_address')

    opt_secret = models.CharField(max_length=16, default=pyotp.random_base32)

    def verify_phone(self, save=True):
        self.phone_verified = True
        if save:
            self.save()

    def mail(self, subject, message, from_mail='no-reply@notifications.trymake.com') -> None:
        send_mail(subject=subject, message=message, from_email=from_mail, recipient_list=[self.email])

    def send_template_mail(self, template: str, context: dict) -> None:
        email_template = EMAIL_TEMPLATES[template]
        message = email_template.template.render(context)
        subject = email_template.subject
        from_mail = email_template.from_mail
        self.mail(subject, message, from_mail=from_mail)

    def get_address_list(self) -> QuerySet:
        address_list = self.address_set.all()
        return address_list

    def add_address(self, name: str, long_address: str, city: str,
                    state: 'State', pincode: str, landmark: str, phone: str) -> None:
        address = Address()
        address.customer = self
        address.address = long_address
        address.city = city
        address.phone = phone
        address.landmark = landmark
        address.pincode = pincode
        address.state = state
        address.name = name
        address.save()

    @staticmethod
    def create(email: str, password: str, firstname: str, phone: str) -> 'Customer':
        if User.objects.filter(email=email).exists():
            raise IntegrityError("Email ID Duplicated")
        user = User(username=email,email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        customer = Customer()
        customer.email = email
        customer.user = user
        customer.name = firstname
        customer.phone = phone
        try:
            customer.save()
        except IntegrityError as e:
            customer.user.delete()
            raise e
        Customer._add_group(customer)
        return customer

    @staticmethod
    def create_with_existing_user(user: User, phone: str) -> 'Customer':
        customer = Customer()
        customer.email = user.email
        customer.user = user
        customer.name = "%s %s" % (user.first_name, user.last_name)
        customer.phone = phone
        try:
            customer.save()
        except IntegrityError:
            customer.user.delete()
            raise IntegrityError("Email ID Duplicated")
        Customer._add_group(customer)
        return customer

    @staticmethod
    def _add_group(customer):
        try:
            g = Group.objects.get(name=Customer.GROUP_NAME)
        except Group.DoesNotExist:
            g = Group(name=Customer.GROUP_NAME)
            g.save()
        g.user_set.add(customer.user)
        g.save()

    @classmethod
    def verify(cls, token: str) -> bool:
        try:
            t = UniqueToken.objects.select_related('customer').get(token=token)
        except UniqueToken.DoesNotExist:
            return False
        if t.been_used:
            return False
        if not t.check_type(UniqueToken.EMAIL_VERIFICATION_TOKEN):
            return False
        t.customer.is_verified = True
        t.customer.save()
        t.been_used = True
        t.save()
        t.customer.send_template_mail(EMAIL_VERIFIED, {'customer': t.customer})
        return True

    @classmethod
    def validate_password_token(cls, request, token: str):
        try:
            t = UniqueToken.objects.get(token=token)
        except UniqueToken.DoesNotExist:
            return False
        if t.been_used:
            return False
        if not t.check_type(UniqueToken.PASSWORD_RESET_TOKEN):
            return False
        t.been_used = True
        t.save()
        request.session[cls.PASSWORD_RESET_CUSTOMER] = t.customer_id.hex
        return True

    @property
    def serialize(self) -> dict:
        return {
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "is_active": self.user.is_active,
            "email": self.user.email,
            "phone": self.phone
        }

    def __str__(self) -> str:
        return self.user.username


class Country(models.Model):
    code = models.CharField(max_length=2, unique=True, db_index=True)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class State(models.Model):
    code = models.CharField(max_length=5, unique=True, db_index=True)
    country = models.ForeignKey(Country, db_index=True)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Address(models.Model):
    customer = models.ForeignKey(Customer, db_index=True, on_delete=models.SET_NULL, null=True, unique=False)
    name = models.CharField(max_length=250,  unique=True)
    address = models.TextField()

    phone = models.CharField(validators=[phone_validator], max_length=11)

    pincode = models.CharField(max_length=6, validators=[pin_validator])

    landmark = models.CharField(max_length=500, blank=True)

    city = models.CharField(max_length=500)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = (('customer', 'name'),)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'pincode': self.pincode,
            'landmark': self.landmark,
            'city': self.city,
            'state': self.state.name,
        }

    def __str__(self):
        return "%s %s : %s - %s" % (self.customer.user.first_name,
                                    self.customer.user.last_name,
                                    self.phone,
                                    self.pincode)


class UniqueToken(models.Model):
    EMAIL_VERIFICATION_TOKEN = 1
    PASSWORD_RESET_TOKEN = 2
    CHOICES = (
        (EMAIL_VERIFICATION_TOKEN, "Email Verification Token"),
        (PASSWORD_RESET_TOKEN, "Password Reset Token")
    )
    customer = models.ForeignKey(Customer)
    token = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    been_used = models.BooleanField(default=False)
    date_issued = models.DateTimeField(default=timezone.now)
    type = models.PositiveSmallIntegerField(choices=CHOICES)

    def check_type(self, type: int):
        return self.type == type

    @classmethod
    def create_token(cls, customer_id: str, type: int) -> str:
        token = cls()
        token.customer_id = customer_id
        token.type = type
        token.save()
        return str(token.token)

    def __str__(self):
        return "%s: %s"%(self.customer, str(self.token))
