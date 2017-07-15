"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
import time

from trymake.apps.SMS_manager import MessageSender
from trymake.apps.SMS_manager import SMS

micro_seconds = 1000
start = time.time()
u = MessageSender()
e_message = time.time() - start
s_SMS = time.time()
s = SMS('9447480852', 'Hello')
e_SMS = time.time() - s_SMS
s_send = time.time()
u.send_sms(s)
e_send = time.time() -s_send

print("Part         \t\t\tTime taken")
print("Create sender\t\t\t{0}ms".format(e_message * micro_seconds))
print("Create SMS   \t\t\t{0}ms".format(e_SMS * micro_seconds))
print("send SMS     \t\t\t{0}ms".format(e_send * micro_seconds))
