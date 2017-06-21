from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from trymake.apps.customer.models import Customer
from trymake.apps.product.models import Product


class Wishlist(models.Model):
    customer = models.OneToOneField(Customer)


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist)
    product = models.ForeignKey(Product)
    date_added = models.DateTimeField()


class Feedback(models.Model):
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)
    is_positive = models.BooleanField(default=True)
    comment = models.TextField()
    verified_buyer = models.BooleanField(default=False)


class ProductInStockNotification(models.Model):
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)

