"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

from django.db import models

from trymake.apps.orders_management.models import Order


class Coupon(models.Model):
    COUPON_TYPES = (
        ('FO', "Fixed Amount Off Cart Value"),
        ('PO', "Percentage Off Cart Value"),
        ('FP', "Fixed Amount Off Product"),
        ('PP', "Percentage Off Product")

    )
    code = models.CharField(max_length=6, unique=True, db_index=True)
    description = models.TextField()
    discount = models.PositiveSmallIntegerField()
    type = models.CharField(choices=COUPON_TYPES, max_length=2)
    usage_cap = models.PositiveSmallIntegerField()
    per_user = models.BooleanField()

    @classmethod
    def create(cls, code: str, desc: str, discount: int, type: tuple, usage_cap: int, per_user: bool):
        coupon = cls()
        coupon.code = code
        coupon.description = desc
        coupon.discount = discount
        coupon.type = type
        coupon.usage_cap = usage_cap
        coupon.per_user = per_user
        coupon.save()
        return coupon


class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon)
    order = models.ForeignKey(Order)
