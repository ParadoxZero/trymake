"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
from django.core.exceptions import ValidationError
from django.db import models

from trymake.apps.customer.models import Customer, Address
from trymake.apps.product.models import Product
from trymake.apps.validators import phone_validator


class Cart(models.Model):
    customer = models.ForeignKey(Customer)


class OrderStatus(models.Model):
    name = models.CharField(max_length=100)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    date_placed = models.DateTimeField()
    date_completed = models.DateTimeField()
    is_completed = models.BooleanField()
    order_status = models.CharField(max_length=100)
    last_status_changed = models.DateTimeField()
    address = models.TextField()
    phone = models.CharField(validators=[phone_validator], max_length=11,unique=True)


    @property
    def serialize(self):
        return {
            "order_id": self.id,
            "total_cost": self.total_cost,
            "date_placed": self.date_placed,
            "date_completed": self.date_completed,
            "is_completed": self.is_completed,
            "order_status": self.order_status,
            "address":self.address,
            "phone":self.phone,
        }


class Item(models.Model):
    product = models.ForeignKey(Product)
    qty = models.SmallIntegerField()
    vendor = models.ForeignKey(Customer)
    order = models.ForeignKey(Order)
    cart = models.ForeignKey(Cart)

    def clean(self):
        if self.order == self.cart:
            raise ValidationError("At least and At most Cart or Order should be set")

    @property
    def serialize(self):
        return {
            "product": self.product.serialize,
            "qty":self.qty,
            "vendor": self.vendor,
            "sub_total": "" # TODO
        }