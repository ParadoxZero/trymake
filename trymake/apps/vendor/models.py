"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

import uuid

from datetime import datetime
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db import models
from django.db.models.signals import pre_save

# Create your models here.
from trymake.apps.commons.models import Image
from trymake.apps.product.models import Product


class Vendor(models.Model):
    # Serialize Names
    NAME = 'name'
    EMAIL = 'email'
    DESCRIPTION = 'description'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=500)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User)
    description = models.TextField()

    @classmethod
    def create_vendor(cls, name, email, password, description):
        if User.objects.filter(email=email).exists():
            raise IntegrityError("Email ID Duplicated")
        vendor = cls()
        vendor.name = name
        vendor.email = email
        vendor.user = User.objects.create_user(username=email, email=email, password=password)
        vendor.user.save()

    @property
    def serialize(self):
        return {

        }


class ReturnPolicy(models.Model):
    vendor = models.ForeignKey(Vendor)
    return_by = models.PositiveSmallIntegerField()  # Number of days
    terms_and_conditions = models.TextField()


class Stock(models.Model):
    vendor = models.ForeignKey(Vendor, db_index=True)
    product = models.ForeignKey(Product, db_index=True, to_field='slug')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    stock = models.PositiveIntegerField()
    return_policy = models.ForeignKey(ReturnPolicy)
    date_added = models.DateTimeField(default=datetime.now)


# ----------------------- #
# Signals and registering #
# ----------------------- #

def stock_before_created(sender, **kwargs):
    stock = kwargs['instance']
    stock.date_changed = datetime.now()


pre_save.connect(stock_before_created, sender=Stock)
