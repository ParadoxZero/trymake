import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from trymake.apps.commons.models import Image
from trymake.apps.product.models import Product


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=500)
    email = models.EmailField()
    user = models.OneToOneField(User)
    description = models.TextField()

    # TODO def create()


class Stock(models.Model):
    vendor = models.ForeignKey(Vendor, db_index=True)
    product = models.ForeignKey(Product, db_index=True)


