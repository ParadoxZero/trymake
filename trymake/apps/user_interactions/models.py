"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

from django.db import models

from trymake.apps.orders_management.models import Order
from trymake.apps.customer.models import Customer
from trymake.apps.product.models import Product


class Wishlist(models.Model):
    customer = models.OneToOneField(Customer)


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist)
    product = models.ForeignKey(Product)
    date_added = models.DateTimeField()


class ProductFeedback(models.Model):
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)
    is_positive = models.BooleanField(default=True)
    comment = models.TextField()
    verified_buyer = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.verified_buyer = Order.objects.filter(customer=self.customer).filter(item__product=self.product).exists()
        super(ProductFeedback, self).save(force_insert=force_insert, force_update=force_update,
                                          using=using, update_fields=update_fields)


class ProductInStockNotification(models.Model):
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)


class OrderFeedback(models.Model):
    order = models.OneToOneField(Order)
    feedback = models.TextField()


class Feedback(models.Model):
    customer = models.ForeignKey(Customer)
    feedback = models.TextField()
