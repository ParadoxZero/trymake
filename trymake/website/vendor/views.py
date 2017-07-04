"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_POST

from trymake.apps.commons.models import Image
from trymake.apps.product.models import AdditionalImages
from trymake.website import utils
from trymake.website.utils import form_validation_error
from trymake.website.vendor.forms import ProductAddForm, AdditionalImagesForm


# TODO add vendor_login_required to all views

def index(request):
    return render(request, 'website/vendor/index.html', {
        'product': ProductAddForm(),
        'additional_images': AdditionalImagesForm()
    })


@require_POST
def product_add(request):
    form = ProductAddForm(request.POST, request.FILES)
    print(request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse({utils.KEY_STATUS: utils.STATUS_OKAY})
    else:
        return form_validation_error(form)


@require_POST
def image_add(request, product_slug):
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        form.save_image(product_slug)
        return JsonResponse({
            utils.KEY_STATUS: utils.STATUS_OKAY
        })
    else:
        return form_validation_error(form)
