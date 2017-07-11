"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from trymake.apps.customer.models import Customer, EMAIL_WELCOME


@receiver(pre_save, sender=User)
def set_inactive(sender: User, **kwargs):
    sender.is_active = False
    print(kwargs)


@receiver(post_save, sender=Customer)
def send_welcome_message(sender: Customer, **kwargs):
    sender.send_template_mail(EMAIL_WELCOME,{'customer':sender})
    print(kwargs)


@receiver(post_save, sender=Customer)
def sync_email(sender:Customer, **kwargs):
    Customer.user.email = sender.email
    Customer.user.save()
    print(kwargs)

