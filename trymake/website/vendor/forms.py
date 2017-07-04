"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
from django import forms

from trymake.apps.product.models import Product


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['additional_images']