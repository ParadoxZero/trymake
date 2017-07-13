"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
from trymake.apps.SMS_manager import SMS


class SmsBackend:
    def __init__(self):
        self.data = {
            'sender_id': "Trymake"
        }

    def send_sms(self, phone_number, message):
        self.data['to'] = phone_number,
        self.data['message'] = message,
        print(self.data)