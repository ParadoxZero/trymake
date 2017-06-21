from django.db import models

from trymake.apps.customer.models import State
from trymake.apps.product.models import Product

FLAT_RATE = 'fr'
ZONE_BASED = 'zb'

TYPES_CHOICES = (
    (FLAT_RATE, "Flat Rate"),
    (ZONE_BASED, "Zone Based")
)


class DeliveryOption(models.Model):
    name = models.CharField(max_length=500)
    type = models.CharField(max_length=2, choices=TYPES_CHOICES)
    product = models.ManyToManyField(Product)


class FlatRateDelivery(models.Model):
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_option = models.ForeignKey(DeliveryOption)


class Zone(models.Model):
    zone_name = models.CharField(max_length=500)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    inclusive_states = models.ManyToManyField(State)
