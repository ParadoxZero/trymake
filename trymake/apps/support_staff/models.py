from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

from trymake.apps.commons.models import Permissions


class Staff(models.Model):
    user = models.OneToOneField(User)
    permission = models.ForeignKey(Permissions)
    name = models.CharField(max_length=250)
    email = models.EmailField()

    phone_validator = RegexValidator(regex=r"[0-9]{10}", message="Format: 9999999999")
    phone = models.CharField(validators=[phone_validator], max_length=11,unique=True)