"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Trymake Inc
All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Image(models.Model):
    name = models.CharField(max_length=250, unique=True, db_index=True)
    image = models.ImageField(upload_to="images")
    date_added = models.DateTimeField()

    # TODO def create(upload_to, name, image, date)
    # TODO def delete_image()


class Permissions(models.Model):
    orders = models.BooleanField()
    complaints = models.BooleanField()
    customer_email = models.BooleanField()
    comments = models.BooleanField()
    # TODO add more permissions
