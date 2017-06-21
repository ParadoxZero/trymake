from django.db import models

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

    order = models.ForeignKey(Order,db_index=True)
    title = models.CharField(max_length=250)
    body = models.TextField()
    date_published = models.DateTimeField()
    last_change = models.DateTimeField()
    date_closed = models.DateTimeField() # Resolved or Canceled can be counted as closed
    status = models.PositiveSmallIntegerField(choices=CHOICES)
    assigned = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)
