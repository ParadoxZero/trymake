"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
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

    @property
    def serialize(self):
        return {
            'name': self.name,
            'image_url': self.image.url
        }
