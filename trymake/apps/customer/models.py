import uuid

from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from django.db import IntegrityError
from django.db import models


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.OneToOneField(User, unique=True)
    email = models.EmailField(unique=True, null=False, db_index=True)
    is_verified = models.BooleanField(default=False)

    phone_validator = RegexValidator(regex=r"[0-9]{10}", message="Format: 9999999999")
    phone = models.CharField(validators=[phone_validator], max_length=11,unique=True)

    @staticmethod
    def create(username: str, email: str, password: str, firstname: str, lastname: str):
        customer = Customer()
        customer.email = email
        customer.user = User.objects.create_user(username, email, password)
        customer.user.last_name = lastname
        customer.user.first_name = firstname
        customer.user.save()
        try:
            g = Group.objects.get(name="Customer")
        except Group.DoesNotExist:
            g = Group(name="Customer")
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
    code = models.CharField(max_length=2,unique=True)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class State(models.Model):
    code = models.CharField(max_length=2,unique=True)
    country = models.ForeignKey(Country, db_index=True)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Address(models.Model):
    customer = models.ForeignKey(Customer, db_index=True)
    name = models.CharField(max_length=255)
    address = models.TextField()

    phone_validator = RegexValidator(regex=r"[0-9]{10}", message="Format: 9999999999")
    phone = models.CharField(validators=[phone_validator], max_length=11)

    pin_validator = RegexValidator(regex=r"[0-9]{6}", message="Format: 999999")
    pincode = models.CharField(max_length=6, validators=[pin_validator])

    landmark = models.CharField(max_length=500, blank=True)

    city = models.CharField(max_length=500)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s %s : %s - %s"%(self.customer.user.first_name,
                                  self.customer.user.last_name,
                                  self.phone,
                                  self.pincode)
