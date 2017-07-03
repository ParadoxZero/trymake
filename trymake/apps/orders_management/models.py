"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

from trymake.apps.customer.models import Customer, Address
from trymake.apps.product.models import Product
from trymake.apps.validators import phone_validator
from trymake.apps.vendor.models import Stock, Vendor


class Cart(models.Model):
    customer = models.OneToOneField(Customer, db_index=True)
    date_changed = models.DateTimeField()

    def add_item(self, sku: int, qty: int):
        vendor_stock = Stock.objects.get(pk=sku)
        return Item.create_item(vendor_stock.product_id, qty, vendor_stock.vendor_id, self.id, vendor_stock.vendor.name,
                                vendor_stock.product.name, vendor_stock.price)

    @transaction.atomic
    def update_price(self):
        item_list = Item.objects.filter(cart=self)
        stock_list = Stock.objects.filter(product_id__in=[item.product_id for item in item_list])
        for item in item_list:
            item.price = stock_list.get(product_id=item.product_id).price
            item.save()

    @transaction.atomic
    def clear_cart(self):
        Item.objects.filter(cart=self).delete()
        self.date_changed = timezone.now()
        self.save()

    def buy(self, order_id: int):
        item_list = Item.objects.filter(cart=self).update(cart=None, order_id=order_id)


class Order(models.Model):
    # Serialized Order Constants.
    PHONE = 'phone'
    ADDRESS = 'address'
    ORDER_STATUS = 'order_status'
    IS_COMPLETED = 'is_completed'
    DATE_COMPLETED = 'date_completed'
    DATE_PLACED = 'date_placed'
    TOTAL_COST = 'total_cost'
    ORDER_ID = 'order_id'

    # Order status and choices
    ORDER_RECEIVED = 0
    AWAITING_PAYMENT = 1
    PROCESSING = 2
    SHIPPED = 3
    WAITING_RETURN = 4
    PROCESSING_REFUND = 5
    RETURNED = 6
    COMPLETED = 7
    CANCELLED = 8
    REJECTED = 9

    ORDER_STATUS_CHOICES = (
        (ORDER_RECEIVED, "Order Received"),
        (AWAITING_PAYMENT, "Awaiting Payment"),
        (PROCESSING, "Processing"),
        (SHIPPED, "Shipped"),
        (WAITING_RETURN, "Waiting Return"),
        (PROCESSING_REFUND, "Processing Refund"),
        (RETURNED, "Returned"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
        (REJECTED, "Rejected")
    )

    # Model Fields
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, db_index=True)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    date_placed = models.DateTimeField()
    date_completed = models.DateTimeField()
    is_completed = models.BooleanField()
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default=ORDER_RECEIVED)
    last_status_changed = models.DateTimeField()
    address = models.TextField()
    phone = models.CharField(validators=[phone_validator], max_length=11, unique=True)

    @staticmethod
    def get_order_details(customer_id, completed, cancelled, num, chunk_number):
        order_list = Order.objects.filter(customer_id=customer_id).prefetch_related('item_set')
        if completed:
            order_list = order_list.filter(order_status=Order.COMPLETED)
        if cancelled:
            order_list = order_list.filter(order_status=Order.CANCELLED)
        order_list = order_list[num*chunk_number:num*(chunk_number+1)]
        return [{'order_details': order.serialize,
                 'order_items': [item.serialize for item in order.item_set]} for order in order_list]

    @property
    def serialize(self):
        return {
            self.ORDER_ID: self.id,
            self.TOTAL_COST: self.total_cost,
            self.DATE_PLACED: self.date_placed,
            self.DATE_COMPLETED: self.date_completed,
            self.IS_COMPLETED: self.is_completed,
            self.ORDER_STATUS: self.order_status,
            self.ADDRESS: self.address,
            self.PHONE: self.phone,
        }


class Item(models.Model):
    # Serialized Constants
    SUB_TOTAL = 'sub_total'
    PRICE = 'price'
    VENDOR = 'vendor'
    QTY = 'qty'
    PRODUCT = 'product'
    PRODUCT_ID = 'product_id'
    VENDOR_ID = 'vendor_id'

    # Model fields
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    qty = models.SmallIntegerField()
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, db_index=True)
    cart = models.ForeignKey(Cart, db_index=True)
    # Redundant:
    # In case the product or vendor is deleted from the database
    vendor_name = models.CharField(max_length=250)
    product_name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def clean(self):
        if self.order == self.cart:
            raise ValidationError("At least and At most only Cart or Order should be set")

    @classmethod
    def create_item(cls, product_id: int, qty: int, vendor_id: int, cart_id: int,
                    vendor_name: str, product_name: str, price: Decimal) -> 'Item':
        item = cls()
        item.product_id = product_id
        item.qty = qty
        item.vendor_id = vendor_id
        item.cart_id = cart_id
        item.vendor_name = vendor_name
        item.price = price
        item.product_name = product_name
        item.save()
        return item

    @property
    def serialize(self):
        return {
            self.PRODUCT: self.product_name,
            self.QTY: self.qty,
            self.VENDOR: self.vendor_name,
            self.PRICE: self.price,
            self.SUB_TOTAL: self.price * self.qty,
            self.VENDOR_ID: self.vendor_id,
            self.PRODUCT_ID: self.product_id
        }