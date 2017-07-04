"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from trymake.website.vendor.forms import ProductAddForm


def index(request):
    return render(request,'website/vendor/index.html',{'product':ProductAddForm()})


def product_add(request):
    form = ProductAddForm(request.POST, request.FILES)
    print(request.FILES)
    if form.is_valid():
        form.save()
    else:
        return HttpResponse(str(form.errors))
    return HttpResponse("hello")