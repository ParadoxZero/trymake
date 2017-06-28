"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Trymake Inc
All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

from django.db import models

from trymake.apps.customer.models import Customer, Address
from trymake.apps.product.models import Product


class Cart(models.Model):
    customer = models.ForeignKey(Customer)


class OrderStatus(models.Model):
    name = models.CharField(max_length=500)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    date_placed = models.DateTimeField()
    date_completed = models.DateTimeField()
    is_completed = models.BooleanField()
    order_status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)
    last_status_changed = models.DateTimeField()
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)


class Item(models.Model):
    product = models.ForeignKey(Product)
    qty = models.SmallIntegerField()
    vendor = models.ForeignKey(Customer)
    order = models.ForeignKey(Order)
    cart = models.ForeignKey(Cart)
