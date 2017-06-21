from django.db import models

from trymake.apps.customer.models import Customer
from trymake.apps.product.models import Product


class Cart(models.Model):
    customer = models.ForeignKey(Customer)


class OrderStatus(models.Model):
    name = models.CharField(max_length=500)


class Order(models.Model):
    customer = models.ForeignKey(Customer)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    date_placed = models.DateTimeField()
    date_completed = models.DateTimeField()
    is_completed = models.BooleanField()
    order_status = models.ForeignKey(OrderStatus)
    last_status_changed = models.DateTimeField()


class Item(models.Model):
    product = models.ForeignKey(Product)
    qty = models.SmallIntegerField()
    vendor = models.ForeignKey(Customer)
    order = models.ForeignKey(Order)
    cart = models.ForeignKey(Cart)
