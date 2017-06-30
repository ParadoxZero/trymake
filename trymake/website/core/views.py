"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Trymake Inc
All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from trymake import settings
from trymake.apps.complaints.models import Complaint
from trymake.apps.customer.models import Customer, Address
from trymake.apps.orders_management.models import Order

from trymake.website.core import utils
from trymake.website.core.forms import EnterEmailForm, RegistrationForm, LoginForm, AddressForm, FeedbackForm
from trymake.website.core.utils import get_context, redirect_to_origin
from trymake.website.core.decorators import require_logged_out, customer_login_required


#################################################################################
# Core website Views                                                            #
# ----------------------------------------------------------------------------- #
# Every template in the core segment has                                        #
# few common context data                                                       #
#                                                                               #
# They are:                                                                     #
# 1) Message                                                                    #
# 2) Error Message                                                              #
# 3) Login Form                                                                 #
# 4) Registration Form                                                          #
# 5) Users                                                                      #
#                                                                               #
# The context name for them can be referenced from                              #
# trymake.website.core.utils                                                    #
#                                                                               #
#################################################################################


def index(request):
    context = get_context(request)
    context["address_form"] = AddressForm()
    return render(request, 'website/core/index.html', context)


#################################################################################
# Login views                                                                   #
# ----------------------------------------------------------------------------- #
#                                                                               #
# Trymake Login flow in four phases/parts:                                      #
#     1) user enters email                                                      #
#     2) if email exists in database, show password field                       #
#     3) email exists, but not verified, show resend verification link          #
#     4) if email doesn't exist, show registration field                        #
#                                                                               #
#################################################################################

@require_POST
@require_logged_out
def check_account_exists(request):
    """
    Request will be originated from login phase one.
    """
    form = EnterEmailForm(request)
    if form.is_valid():
        exists = Customer.objects.filter(email=form.cleaned_data['email']).exists()
        if exists:
            return JsonResponse({"status": "OK", "exists": True})
        else:
            return JsonResponse({"status": "OK", "exists": False})
    return JsonResponse({"status": "fail", "reason": utils.ERROR_INVALID_INPUT})


@require_POST
@require_logged_out
def process_login(request):
    """
    Login phase two when email exists
    """
    form = LoginForm(request, request.POST)
    if form.is_valid():
        user = form.user
        login(request, user)
        request.session[utils.SESSION_CUSTOMER_ID] = str(form.customer_id)
        print(str(form.customer_id))
    else:
        request.session[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INCORRECT_CREDENTIALS
        if settings.DEBUG:
            print("Debug: ", form.errors)
        request.session[utils.KEY_LOGIN_FORM_DATA] = request.POST
        print(request.session[utils.KEY_LOGIN_FORM_DATA])
    return redirect_to_origin(request)


@require_POST
@require_logged_out
def process_registration(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():
        customer = Customer.create(
            email=form.cleaned_data.get("email"),
            phone=str(form.cleaned_data.get("phone")),
            password=str(form.cleaned_data.get("password")),
            firstname=form.cleaned_data.get("name")
        )
    else:
        print(form.errors)
        request.session[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INVALID_INPUT
        request.session[utils.KEY_REGISTRATION_FORM_DATA] = request.POST
    return redirect_to_origin(request)


def logout_view(request):
    logout(request)

    return HttpResponseRedirect("/")


#################################################################################
# Account Views                                                                 #
# ----------------------------------------------------------------------------- #
#                                                                               #
# Consists of the following pages which will load templates:                    #
#                                                                               #
#   1) My Account page                                                          #
#   2) My orders                                                                #
#   3) Add or edit my Address - AddressForm                                     #
#   4) Edit Profile - UpdateProfileForm(),ChangePasswordForm()                  #
#                                                                               #
#################################################################################


@customer_login_required
def my_account(request):
    context = get_context(request)
    context['orders'] = Order.objects.filter(customer__user=request.user).order_by('-date_placed')[:3]
    context['customer'] = Customer.objects.get(user=request.user)
    context['complaints'] = Complaint.objects.filter(order__customer__user=request.user)[:3]
    return render(request, 'website/core/my_account.html', context=context)


@customer_login_required
@require_POST
def process_feedback(request):
    form = FeedbackForm(request.POST)
    if form.is_valid():
        customer = Customer.objects.get(user=request.user)
        form.save_feedback(customer)
    else:
        request.session[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INVALID_INPUT
    return redirect_to_origin(request)


@customer_login_required
@require_POST
def process_address_add(request):
    form = AddressForm(request.POST)
    if form.is_valid():
        address = Address(
            name=form.cleaned_data['name'],
            address=form.cleaned_data['address'],
            landmark=form.cleaned_data['landmark'],
            city=form.cleaned_data['city'],
            pincode=form.cleaned_data['pincode'],
            phone=form.cleaned_data['phone'],
            customer_id=request.session[utils.SESSION_CUSTOMER_ID]
        )
        address.save()
    else:
        print(form.errors)
        request.session[utils.KEY_ERROR_MESSAGE]= utils.ERROR_INVALID_ADDRESS
        request.session[utils.KEY_ADDRESS_FORM_DATA] = request.POST
    return redirect_to_origin(request)
