"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Trymake Inc
All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

import uuid

import decimal

from datetime import datetime
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.db import IntegrityError
from django.db import models
from django.db.models.signals import pre_save

# Create your models here.
from trymake.apps.commons.models import Image
from trymake.apps.product.models import Product


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=500)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User)
    description = models.TextField()

    def create_new_product(self, name: str, slug: str, approximate_weight: decimal,
                           short_description: str, long_Description: str,
                           image: UploadedFile, image_name: str, stock: int,
                           price: decimal, discounted_price: decimal):
        product = Product.create_product(name, slug, approximate_weight, short_description,
                                         long_Description, image, image_name)
        stock = Stocks(
            vendor=self,
            product=product,
            price=price,
            discounted_price=discounted_price,
            stock=stock,
        )
        stock.save()

    @classmethod
    def create_vendor(cls, name, email, password, description):
        if User.objects.filter(email=email).exists():
            raise IntegrityError("Email ID Duplicated")
        vendor = cls()
        vendor.name = name
        vendor.email = email
        vendor.user = User.objects.create_user(username=email, email=email, password=password)
        vendor.user.save()


class ReturnPolicy(models.Model):
    vendor = models.ForeignKey(Vendor)
    return_by = models.PositiveSmallIntegerField()  # Number of dates
    terms_and_conditions = models.TextField()


class Stocks(models.Model):
    vendor = models.ForeignKey(Vendor, db_index=True)
    product = models.ForeignKey(Product, db_index=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    stock = models.PositiveIntegerField()
    return_policy = models.ForeignKey(ReturnPolicy)
    date_added = models.DateTimeField(default=datetime.now)
    date_changed = models.DateTimeField()


#### Signals and registering ###

def stock_before_created(sender, **kwargs):
    stock = kwargs['instance']
    stock.date_changed = datetime.now()


pre_save.connect(stock_before_created, sender=Stocks)
