"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
from django.core.validators import RegexValidator

pin_validator = RegexValidator(regex=r"[0-9]{6}", message="Format: 999999")
phone_validator = RegexValidator(regex=r"[0-9]{10}", message="Format: 9999999999")
