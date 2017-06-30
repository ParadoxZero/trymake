"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

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
    context[utils.KEY_REGISTRATION_FORM] = RegistrationForm()
    context[utils.KEY_LOGIN_FORM] = LoginForm()
    context["address_form"] = AddressForm()
    context[utils.KEY_CHECK_EMAIL_FORM] = EnterEmailForm()
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
def check_account_exists(request):  # AJAX
    """
    Request will be originated from login phase one.
    """
    print(request.body)
    response = dict()
    form = EnterEmailForm(request.POST)
    if form.is_valid():
        response[utils.KEY_STATUS] = utils.STATUS_OKAY
        response[utils.KEY_EMAIL] = form.cleaned_data['email']
        if Customer.objects.filter(email=form.cleaned_data['email']).exists():
            response[utils.KEY_EMAIL_REGISTERED] = True
        else:
            response[utils.KEY_EMAIL_REGISTERED] = False
    else:
        response[utils.KEY_STATUS] = utils.STATUS_ERROR
        response[utils.KEY_ERROR_MESSAGE] = form.errors
        response[utils.KEY_FORM] = form.as_table()
    return JsonResponse(response)


@require_POST
@require_logged_out
def process_login(request):  # AJAX
    """
    Login phase two when email exists
    """
    form = LoginForm(request, request.POST)
    response = dict()
    if form.is_valid():
        user = form.user
        login(request, user)
        if not form.cleaned_data['remember_me']:
            request.session.set_expiry(0)
        request.session[utils.SESSION_CUSTOMER_ID] = str(form.customer_id)
        response[utils.KEY_STATUS] = utils.STATUS_OKAY
    else:
        response[utils.KEY_STATUS] = utils.STATUS_ERROR
        response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INCORRECT_CREDENTIALS
        response[utils.KEY_LOGIN_FORM] = form.as_table()
    return JsonResponse(response)


@require_POST
@require_logged_out
def process_registration(request):  # AJAX
    response = dict()
    form = RegistrationForm(request.POST)
    if form.is_valid():
        customer = Customer.create(
            email=form.cleaned_data.get("email"),
            phone=str(form.cleaned_data.get("phone")),
            password=str(form.cleaned_data.get("password")),
            firstname=form.cleaned_data.get("name")
        )
        response[utils.KEY_STATUS] = utils.STATUS_OKAY
    else:
        response[utils.KEY_STATUS] = utils.STATUS_ERROR
        response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INVALID_INPUT
        response[utils.KEY_REGISTRATION_FORM] = form.as_table()
    return JsonResponse(response)


def logout_view(request):  # AJAX
    logout(request)
    request.session.flush()

    # It is necessary to redirect so that any settings or any information
    # related to the previous user which may have existed in the javascript
    # Or cookies in general is flushed and removed.
    return HttpResponseRedirect(reverse("core:index"))


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
def my_account(request):  # Template
    context = get_context(request)
    context['orders'] = Order.objects.filter(customer__user=request.user).order_by('-date_placed')[:3]
    context['customer'] = Customer.objects.get(user=request.user)
    context['complaints'] = Complaint.objects.filter(order__customer__user=request.user)[:3]
    return render(request, 'website/core/my_account.html', context=context)


# ---------------------- #
# Feedback Forms Related #
# ---------------------- #

@customer_login_required
@require_POST
def get_feedback_form(request):
    return JsonResponse({
        utils.KEY_STATUS: utils.STATUS_OKAY,
        utils.KEY_FORM: FeedbackForm().as_table()
    })


@customer_login_required
@require_POST
def process_feedback(request):  # AJAX
    response = dict()
    form = FeedbackForm(request.POST)
    if form.is_valid():
        response[utils.KEY_STATUS] = utils.STATUS_OKAY
        customer = Customer.objects.get(user=request.user)
        form.save_feedback(customer)
    else:
        response[utils.KEY_STATUS] = utils.STATUS_ERROR
        response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INVALID_INPUT
        response[utils.KEY_FORM] = form.as_table()
    return JsonResponse(response)


# -------------------- #
# Address Form Related #
# -------------------- #

# If the request contains the name of an address
# The form will return form with the details of
# address pre-filled otherwise it will return a
# blank form.
@customer_login_required
@require_POST
def get_address_form(request):  # AJAX
    response = dict()
    response[utils.KEY_STATUS] = utils.STATUS_OKAY
    if utils.KEY_ADDRESS_NAME in request.POST:
        address_list = Address.objects.filter(name=request.POST[utils.KEY_ADDRESS_NAME])
        if len(address_list) > 0:
            address = address_list.first()  # type:Address
            form = AddressForm(initial={
                "name": address.name,
                "phone": address.phone,
                "address": address.address,
                "pincode": address.pincode,
                "landmark": address.landmark,
                "city": address.city,
                "state": address.state
            })
            response[utils.KEY_FORM] = form.as_table()
        else:
            response[utils.KEY_STATUS] = utils.STATUS_ERROR
            response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_ADDRESS_NOT_FOUND
            response[utils.KEY_ADDRESS_NAME] = request.POST[utils.KEY_ADDRESS_NAME]
    else:
        response[utils.KEY_FORM] = AddressForm().as_table()
    return JsonResponse(response)


# Only handles creation of new address
# In case the given address name already exists.
@customer_login_required
@require_POST
def process_address_add(request):  # AJAX
    response = dict()
    form = AddressForm(request.POST)
    response[utils.KEY_STATUS] = utils.STATUS_OKAY
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
        response[utils.KEY_ADDRESS_NAME] = address.name
        try:
            address.save()
        except IntegrityError:
            response[utils.KEY_STATUS] = utils.STATUS_ERROR
            response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_ADDRESS__NAME_EXISTS
            response[utils.KEY_FORM] = form.as_table()
    else:
        response[utils] = utils.STATUS_ERROR
        response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INVALID_ADDRESS
        response[utils.KEY_FORM] = form.as_table()
    return JsonResponse(response)
