"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

from django.db import models
from django.utils import timezone

from trymake.apps.orders_management.models import Order
from trymake.apps.support_staff.models import Staff


class Complaint(models.Model):
    RESOLVED = 1
    WAITING = 2
    PROCESSING = 3
    CANCELED = 4
    CHOICES = (
        (RESOLVED, "Resolved"),
        (WAITING, "Waiting"),
        (PROCESSING, "Processing"),
        (CANCELED, "Canceled")
    )

    order = models.ForeignKey(Order, db_index=True)
    title = models.CharField(max_length=250)
    body = models.TextField()
    date_published = models.DateTimeField()
    last_change = models.DateTimeField(null=True)
    date_closed = models.DateTimeField(null=True)  # Resolved or Canceled can be counted as closed
    status = models.PositiveSmallIntegerField(choices=CHOICES)
    assigned = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)

    @classmethod
    def register_complaint(cls, order_id: str, title: str, body: str):
        c = cls()
        c.order_id = order_id
        c.title = title
        c.body = body
        c.date_published = timezone.now()
        c.status = c.WAITING
        c.save()
        return c

    @property
    def serialize(self):
        return {
            "order_id": self.order_id,
            "title": self.title,
            "body": self.body,
            "date_published": self.date_published,
            "last_change_date": self.last_change,
            "date_closed": self.date_closed,
            "status": dict(Complaint.CHOICES)[self.status],
            "assigned": self.assigned.name
        }
