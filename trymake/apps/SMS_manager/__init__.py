"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
import importlib

from django.conf import settings

import trymake.apps.SMS_manager.backends


class SMS:
    def __init__(self, phone_number, message):
        self.phone_number = phone_number
        self.message = message


class MessageSender:
    def __init__(self):
        backend = settings.SMS_BACKEND  # type:str
        module_name, class_name = backend.rsplit(".", 1)
        module_ = importlib.import_module(module_name)
        self.sms_sender = getattr(module_, class_name)()

    def send_sms(self, sms: SMS):
        self.sms_sender.send_sms(sms.phone_number, sms.message)
