from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Image(models.Model):
    name = models.CharField(max_length=250, unique=True, db_index=True)
    image = models.ImageField(upload_to="images")
    date_added = models.DateTimeField()

    # TODO def create(upload_to, name, image, date)
    # TODO def delete_image()


class AdminPermission(models.Model):
    orders = models.BooleanField()
    complaints = models.BooleanField()
    customer_email = models.BooleanField()
    comments = models.BooleanField()
    # TODO add more permissions
