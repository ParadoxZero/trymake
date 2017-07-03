"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

from django.contrib.auth import login, logout
from django.db import IntegrityError, transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET

from trymake.apps.complaints.models import Complaint
from trymake.apps.customer.models import Customer, Address
from trymake.apps.orders_management.models import Order
from trymake.apps.user_interactions.models import ProductFeedback, OrderFeedback
from trymake.website import utils
from trymake.website.core.forms import EnterEmailForm, RegistrationForm, LoginForm, AddressForm, FeedbackForm, \
    UpdateProfileForm, ProductFeedbackForm, OrderFeedbackForm
from trymake.website.utils import redirect_to_origin
from trymake.website.utils.decorators import require_logged_out, customer_login_required


#################################################################################
# Core website Views                                                            #
# ----------------------------------------------------------------------------- #
# There will be only 5 views that renders template.                             #
#                                                                               #
#  1) Homepage ( index )                                                        #
#  2) My-account                                                                #
#  3) Store page ( product listing page)                                        #
#  4) Cart                                                                      #
#  5) Proceed to buy                                                            #
#                                                                               #
# ----------------------------------------------------------------------------- #
# Each of the template pages will have some common                              #
# context variables                                                             #
#                                                                               #
#  1) KEY_USER: authenticated user or None                                      #
#  2) KEY_MESSAGE: if a message needs to be shows.                              #
#  3) KEY_ERROR_MESSAGE: if some error occured in previous request              #
#  4) KEY_FORM: if an errored form was submited earlier                         #
#                   eg. Login form validation failed.                           #
#                                                                               #
# There MAY be a session value util.SESSION_PAGE_DETAIL.                        #
# This session data will contain any message or errors that needs to be shown,  #
# this value is set before redirecting to a view                                #
# SESSION_PAGE_DETAILS may contain few keys like MESSAGE, ERROR, FORM etc       #
#################################################################################


def index(request):  # TEMPLATE
    context = {utils.KEY_USER: request.user if request.user.is_authenticated() else None,
               utils.KEY_REGISTRATION_FORM: RegistrationForm(), utils.KEY_LOGIN_FORM: LoginForm(),
               "address_form": AddressForm(), utils.KEY_CHECK_EMAIL_FORM: EnterEmailForm()}
    return render(request, 'website/core/login.html', context)


@customer_login_required
def my_account(request):  # Template
    """
     Will render the  myaccount page template.
     Will refer page details if found.
     Page details are set while redirecting to the page.
    """

    # If key doesn't exists. That means, it wasn't a redirect
    # Retrieving data structure containing page details
    context = request.session.pop(utils.SESSION_PAGE_DETAIL, dict())
    context['orders'] = Order.objects.filter(customer__user=request.user).order_by('-date_placed')[:3]
    context['customer'] = Customer.objects.get(user=request.user)
    context['complaints'] = Complaint.objects.filter(order__customer__user=request.user)[:3]
    return render(request, 'website/core/my_account.html', context=context)


#################################################################################
# Redirect Views                                                                #
# ----------------------------------------------------------------------------- #
# These views redirect the user to some other link                              #
# depending on the request                                                      #
#                                                                               #
#  1) Login                                                                     #
#  2) Logout                                                                    #
#  3) Payment                                                                   #
#                                                                               #
#################################################################################

@require_POST
@require_logged_out
def process_login(request):  # REDIRECT
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
    request.session[utils.SESSION_PAGE_DETAIL] = response
    return redirect_to_origin(request)


def logout_view(request):  # REDIRECT
    logout(request)
    request.session.flush()

    # It is necessary to redirect so that any settings or any information
    # related to the previous user which may have existed in the javascript
    # Or cookies in general is flushed and removed.
    return HttpResponseRedirect(reverse("core:index"))


#################################################################################
# AJAX Login views                                                              #
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
def is_Logged_in(request):  # AJAX
    response = dict()
    response[utils.KEY_STATUS] = utils.STATUS_OKAY
    response[utils.KEY_IS_AUTHENTICATED] = request.user.is_authenticated()
    return JsonResponse(response)


@require_POST
@require_logged_out
def check_account_exists(request):  # AJAX
    """
    Request will be originated from login phase one.
    """
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
    print(response)
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
        response[utils.KEY_NAME] = customer.user.first_name
    else:
        response[utils.KEY_STATUS] = utils.STATUS_ERROR
        response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INVALID_INPUT
        response[utils.KEY_REGISTRATION_FORM] = form.as_table()
    return JsonResponse(response)


#################################################################################
# AJAX Account Views                                                            #
# ----------------------------------------------------------------------------- #
# Handles following functions:                                                  #
#                                                                               #
#  1) Get order list                                                            #
#  2) Get Address List                                                          #
#  3) Get Complaint List                                                        #
#  4) Get order details                                                         #
#  5) Get Complaint Details                                                     #
#                                                                               #
#                                                                               #
#################################################################################


@require_GET
@customer_login_required
def get_order_list(request):
    """
    Possible GET parameters:
    'n' -> default:50 ->Max Number of orders to get
    'complete' -> Get only Completed orders
    'canceled' -> Get only Canceled orders
    'chunk_number` -> default:0
    """
    n = request.GET.get('n', 50)
    complete = request.GET.get('complete', False)
    canceled = request.GET.get('canceled', False)
    chunk_number = request.GET.get('chunk_number', 0)
    finished, order_list = Order.get_order_details(request.session[utils.SESSION_CUSTOMER_ID], complete, canceled,
                                                      n, chunk_number)
    response = {
        utils.KEY_ORDER_LIST: order_list ,
        utils.KEY_STATUS: utils.STATUS_OKAY,
        utils.KEY_FINISHED: finished
    }
    return JsonResponse(response)


@require_POST
@customer_login_required
def cancel_order(request):
    # TODO
    # How to handle multiple vendors with different cancellation policy?
    # Cancel individual items?
    # Most restrictive policy?
    # Confirm with Bitto
    pass


@require_POST
@customer_login_required
def return_order(request):
    # TODO
    # How to handle orders with different return policies?
    # Minimum return days valid?
    # Confirm with Bitto
    pass


#################################################################################
# Account Form processing                                                       #
# ----------------------------------------------------------------------------- #
# Consists of the following forms:                                              #
#                                                                               #
#  1) Profile Form                                                              #
#  2) Feedback Form                                                             #
#  3) Address Form                                                              #
#  4) Product Feedback Form                                                     #
#  5) Order Feedback Form                                                       #
#                                                                               #
#################################################################################

# ----------------------- #
# Customer Profile Update #
# ----------------------- #

@customer_login_required
@require_POST
def get_update_profile_form(request):  # AJAX
    customer = Customer.objects.get(pk=request.session[utils.SESSION_CUSTOMER_ID])  # type: Customer
    return JsonResponse({
        utils.KEY_STATUS: utils.STATUS_OKAY,
        utils.KEY_FORM: UpdateProfileForm(initial={
            "name": customer.user.first_name,
            "phone": customer.phone
        })
    })


@customer_login_required
@require_POST
def update_customer_profile(request):  # AJAX
    form = UpdateProfileForm(request.POST)
    response = dict()
    response[utils.KEY_STATUS] = utils.STATUS_OKAY
    if form.is_valid():
        customer = Customer.objects.get(pk=request.session[utils.SESSION_CUSTOMER_ID])  # type: Customer
        customer.user.first_name = form.cleaned_data['name']
        customer.phone = form.cleaned_data['phone']
        customer.save()
    else:
        response[utils.KEY_STATUS] = utils.STATUS_ERROR
        response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INVALID_INPUT
        response[utils.KEY_FORM] = form.as_table()
    return JsonResponse(response)


# ---------------------- #
# Feedback Forms Related #
# ---------------------- #

@customer_login_required
@require_POST
def get_feedback_form(request):  # AJAX
    return JsonResponse({
        utils.KEY_STATUS: utils.STATUS_OKAY,
        utils.KEY_FORM: ProductFeedbackForm().as_table()
    })


@customer_login_required
@require_POST
def process_product_feedback(request, product_id: str):
    response = dict()
    response[utils.KEY_STATUS] = utils.STATUS_OKAY
    form = ProductFeedbackForm(request.POST)
    if form.is_valid():
        try:
            form.save_feedback(request.session[utils.SESSION_CUSTOMER_ID], int(product_id))
        except IntegrityError:
            response = {
                utils.KEY_STATUS: utils.STATUS_ERROR,
                utils.KEY_ERROR_MESSAGE: utils.ERROR_ALREADY_EXISTS
            }
    else:
        response = {
            utils.KEY_STATUS: utils.STATUS_ERROR,
            utils.KEY_ERROR_MESSAGE: utils.ERROR_INVALID_INPUT,
            utils.KEY_FORM: form.as_table()
        }
    return JsonResponse(response)


# ------------------------ #
# Product Feedback related #
# ------------------------ #

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


def get_product_feedback_form(request):
    return JsonResponse({
        utils.KEY_FORM: ProductFeedback(),
        utils.KEY_STATUS: utils.STATUS_OKAY
    })


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
        # TODO refactor it into a method in model
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
            response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_ALREADY_EXISTS
            response[utils.KEY_FORM] = form.as_table()
    else:
        response[utils] = utils.STATUS_ERROR
        response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INVALID_INPUT
        response[utils.KEY_FORM] = form.as_table()
    return JsonResponse(response)


# In case the address name doesn't exists for given user,
# Error is thrown.
#
# New address will NOT be created - instead error will be returned.
@customer_login_required
@require_POST
def edit_address(request):  # AJAX
    form = AddressForm(request.POST)
    response = dict()
    response[utils.KEY_STATUS] = utils.STATUS_OKAY
    if form.is_valid():
        address_ = Address.objects.filter(name=form.cleaned_data['name'],
                                          customer_id=request.session[utils.SESSION_CUSTOMER_ID])
        if len(address_) > 0:  # TODO Convert to model method
            address = address_.first()  # type: Address
            address.address = form.cleaned_data['address']
            address.phone = form.cleaned_data['phone']
            address.landmark = form.cleaned_data['landmark']
            address.city = form.cleaned_data['city']
            address.state = form.cleaned_data['state']
            address.save()
            response[utils.KEY_ADDRESS_NAME] = address.name
        else:
            response[utils.KEY_STATUS] = utils.STATUS_ERROR
            response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_ADDRESS_NOT_FOUND
    else:
        response[utils.KEY_STATUS] = utils.STATUS_ERROR
        response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INVALID_INPUT
        response[utils.KEY_FORM] = form.as_table()
    return JsonResponse(response)


# ------------------- #
# Order Feedback Form #
# ------------------- #


@require_POST
@customer_login_required
def get_order_feedback_form(request):
    return JsonResponse({
        utils.KEY_FORM: OrderFeedbackForm(),
        utils.KEY_STATUS: utils.STATUS_OKAY
    })


@require_POST
@customer_login_required
def process_order_feedback(request, order_id):
    form = OrderFeedbackForm(request.POST)
    response = dict()
    response[utils.KEY_STATUS] = utils.STATUS_OKAY
    if form.is_valid():
        form.save_feedback(order_id)
    else:
        response[utils.KEY_STATUS] = utils.STATUS_OKAY
        response[utils.KEY_FORM] = form.as_table()
        response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INVALID_INPUT
    return JsonResponse(response)
