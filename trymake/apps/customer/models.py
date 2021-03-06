"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

import uuid

from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from django.db import IntegrityError
from django.db import models

from trymake.apps.validators import phone_validator, pin_validator


class Customer(models.Model):
    GROUP_NAME = "Customer"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.OneToOneField(User, unique=True)
    email = models.EmailField(unique=True, null=False, db_index=True)
    is_verified = models.BooleanField(default=False)

    phone_validator = RegexValidator(regex=r"[0-9]{10}", message="Format: 9999999999")
    phone = models.CharField(validators=[phone_validator], max_length=11, unique=True)

    def send_mail(self, subject, message):
        # TODO
        pass

    def get_address_list(self):
        address_list = Address.objects.filter(customer=self)
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
        customer = Customer()
        customer.email = email
        customer.user = User.objects.create_user(email, email, password)
        customer.user.first_name = firstname
        customer.phone = phone
        customer.user.save()
        try:
            g = Group.objects.get(name=Customer.GROUP_NAME)
        except Group.DoesNotExist:
            g = Group(name=Customer.GROUP_NAME)
            g.save()
        try:
            customer.save()
        except IntegrityError:
            customer.user.delete()
            raise IntegrityError("Email ID Duplicated")
        g.user_set.add(customer.user)
        g.save()
        return customer

    @property
    def serialize(self):
        return {
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "is_active": self.user.is_active,
            "email": self.user.email
        }

    def __str__(self):
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
    customer = models.ForeignKey(Customer, db_index=True, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=250)
    address = models.TextField()

    phone = models.CharField(validators=[phone_validator], max_length=11)

    pincode = models.CharField(max_length=6, validators=[pin_validator])

    landmark = models.CharField(max_length=500, blank=True)

    city = models.CharField(max_length=500)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)

    default = models.BooleanField(default=False)

    class Meta:
        unique_together = (('default', 'customer'), ('customer', 'name'))

    def __str__(self):
        return "%s %s : %s - %s" % (self.customer.user.first_name,
                                    self.customer.user.last_name,
                                    self.phone,
                                    self.pincode)
