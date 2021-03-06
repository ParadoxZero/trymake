"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
from django import forms
from django.core.exceptions import ValidationError

from trymake import settings
from trymake.apps.commons.models import Image
from trymake.apps.product.models import Product, AdditionalImages


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['additional_images']

    # Checking if the upload size is within Max Upload size
    def clean_product_image(self):
        image = self.cleaned_data['product_image']
        if image.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError("File size lmit exceeded.", 'upload_limit_exeeded')


class AdditionalImagesForm(forms.ModelForm):
    class Meta:
        model = AdditionalImages
        exclude = ['date_added','product']

    def save_image(self,product_slug):
        self.instance.product_slug = product_slug
        return self.save()