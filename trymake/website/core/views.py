"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from social_core.tests.models import User

from trymake.apps.complaints.models import Complaint
from trymake.apps.customer.models import Customer, Address
from trymake.apps.orders_management.models import Order
from trymake.apps.user_interactions.models import ProductFeedback
from trymake.website import utils
from trymake.website.core.forms import EnterEmailForm, RegistrationForm, LoginForm, AddressForm, FeedbackForm, \
    UpdateProfileForm, ProductFeedbackForm, OrderFeedbackForm, RegisterComplaint, OAuthAdditionalForm
from trymake.website.core.utils import send_verification_email
from trymake.website.utils import redirect_to_origin, form_validation_error, get_template_context
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
#  4) KEY_LOGIN_FORM: Contains Login form/ either fresh or errored.             #
#  5) KEY_REGISTRATION_FORM: same as login form                                 #
#                                                                               #
#################################################################################


def index(request):  # TEMPLATE
    context = get_template_context(request)
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
    context = get_template_context(request)
    context['orders'] = Order.get_order_details(request.session[utils.SESSION_CUSTOMER_ID], num=3)
    context['customer'] = Customer.objects.get(id=request.session[utils.SESSION_CUSTOMER_ID])
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
        request.session[utils.KEY_STATUS] = utils.STATUS_OKAY
    else:
        request.session[utils.KEY_STATUS] = utils.STATUS_ERROR
        request.session[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INCORRECT_CREDENTIALS
        request.session[utils.KEY_LOGIN_FORM] = form.as_table()
    return redirect_to_origin(request)


def logout_view(request):  # REDIRECT
    logout(request)
    request.session.flush()

    # It is necessary to redirect so that any settings or any information
    # related to the previous user which may have existed in the javascript
    # Or cookies in general is flushed and removed.
    return HttpResponseRedirect(reverse("core:index"))


def process_email_verification(request):
    """
    GET params:
    * token
    """
    try:
        token = request.GET['token']
    except KeyError:
        return HttpResponseForbidden()
    if Customer.verify(token):
        request.session[utils.KEY_MESSAGE] = utils.MESSAGE_VERIFICATION_SUCCESSFUL
        return redirect_to_origin(request)
    request.session[utils.KEY_ERROR_MESSAGE] = utils.ERROR_INVALID_TOKEN
    return HttpResponseRedirect(reverse('core:index'))


@login_required
def oauth_create(request):
    c = Customer.objects.filter(user=request.user)
    if c.count() > 0:
        request.session[utils.SESSION_CUSTOMER_ID] = c.first().id.hex
        return HttpResponseRedirect(reverse('core:account:myaccount'))
    if request.method == "GET":
        return render(request, "website/core/phone_form.html", {utils.KEY_FORM: OAuthAdditionalForm()})
    if request.method == "POST":
        form = OAuthAdditionalForm(request.POST)
        if form.is_valid():
            user = request.user  # type: User
            customer = Customer.create_with_existing_user(user, form.cleaned_data['phone'])
            return HttpResponseRedirect(reverse('core:oauth_create'))
        else:
            return render(request, "website/core/phone_form.html", {utils.KEY_FORM: form})


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
        return JsonResponse(response)
    else:
        return form_validation_error(form)


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
        send_verification_email(customer)
        return JsonResponse(response)
    else:
        return form_validation_error(form)


@require_POST
@require_logged_out
def email_verification(request):
    """
    POST params:
    * customer_id
    """
    response = dict()
    customer_id = request.POST['customer_id']
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        response[utils.KEY_STATUS] = utils.STATUS_ERROR
        response[utils.KEY_ERROR_MESSAGE] = utils.ERROR_CUSTOMER_DOES_NOT_EXISTS
        return JsonResponse(response)
    send_verification_email(customer)
    response[utils.KEY_STATUS] = utils.STATUS_OKAY
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

# ------ #
# Orders #
# ------ #

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
        utils.KEY_ORDER_LIST: order_list,
        utils.KEY_STATUS: utils.STATUS_OKAY,
        utils.KEY_FINISHED: finished
    }
    return JsonResponse(response)


@require_POST
@customer_login_required
def return_order(request):
    """
    POST params
    * 'order_id'
    * 'product_id'
    :param request:
    :return:
    """
    try:
        order_id = request.POST['order_id']
        product_slug = require_POST['product_slug']
    except KeyError:
        return JsonResponse({
            utils.KEY_STATUS: utils.STATUS_ERROR,
            utils.KEY_ERROR_MESSAGE: utils.ERROR_MISSING_DATA
        })
    returnable = Order.is_returnable(order_id, product_slug)
    if returnable['is_returnable']:
        item = returnable['item']
        item.return_item()
    return JsonResponse({
        utils.KEY_STATUS: utils.STATUS_OKAY,
        utils.KEY_RETURN_ACCEPTED: returnable['is_returnable']
    })


@require_POST
@customer_login_required
def cancel_order(request):
    """
    POST params:
    * 'order_id'
    """
    try:
        order_id = request.POST['order_id']
        reason = request.POST['reason']
    except KeyError:
        return JsonResponse({
            utils.KEY_STATUS: utils.STATUS_ERROR,
            utils.KEY_ERROR_MESSAGE: utils.ERROR_MISSING_DATA
        })
    order = get_object_or_404(Order, id=order_id)
    return JsonResponse({
        utils.KEY_STATUS: utils.STATUS_OKAY,
        utils.KEY_CANCEL_ACCEPTED: order.cancel(reason)
    })


# ---------- #
# Complaints #
# ---------- #

@customer_login_required
def get_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    return JsonResponse({
        utils.KEY_STATUS: utils.STATUS_OKAY,
        utils.KEY_COMPLAINT: complaint.serialize
    })


@require_GET
@customer_login_required
def get_complaint_list(request):
    """
    GET params
    * 'n'
    * 'resolved'
    * 'chunk_number'
    """
    n = request.GET.get('n', 10)
    is_resolved = request.GET.get('resolved', None)
    chunk_number = request.GET.get('chunk_number', 0)
    response = Complaint.get_list(n, is_resolved, chunk_number, request.session[utils.SESSION_CUSTOMER_ID])
    response[utils.KEY_STATUS] = utils.STATUS_OKAY
    return JsonResponse(response)


# ------- #
# Address #
# ------- #

@require_POST
@customer_login_required
def get_address_list(request):
    customer = Customer.objects.prefetch_related('address_set', 'address_set__state',
                                                 'address_set__state__country').get(
        id=request.session[utils.SESSION_CUSTOMER_ID]
    )
    address_list = customer.get_address_list()
    return JsonResponse({
        utils.KEY_STATUS: utils.STATUS_OKAY,
        utils.KEY_ADDRESS_LIST: [addr.serialize for addr in address_list]
    })


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
            "name": customer.name,
            "phone": customer.phone
        }).as_table()
    })


@customer_login_required
@require_POST
def update_customer_profile(request):  # AJAX
    form = UpdateProfileForm(request.POST)
    response = dict()
    response[utils.KEY_STATUS] = utils.STATUS_OKAY
    if form.is_valid():
        customer = Customer.objects.get(pk=request.session[utils.SESSION_CUSTOMER_ID])  # type: Customer
        customer.name = form.cleaned_data['name']
        customer.phone = form.cleaned_data['phone']
        customer.save()
        return JsonResponse(response)
    else:
        return form_validation_error(form)


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
            return JsonResponse({
                utils.KEY_STATUS: utils.STATUS_ERROR,
                utils.KEY_ERROR_MESSAGE: utils.ERROR_ALREADY_EXISTS
            })
        return JsonResponse(response)
    else:
        return form_validation_error(form)


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
        return JsonResponse(response)
    else:
        return form_validation_error(form)


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
    """
    POST params
    * address_name : optional ( use this if you want to retrieve a pre-filled form, to edit an address )
    """
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
        return JsonResponse(response)
    else:
        return form_validation_error(form)


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
        return JsonResponse(response)
    else:
        return form_validation_error(form)


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
        return JsonResponse(response)
    else:
        return form_validation_error(form)


# ----------------- #
# Complaint related #
# ----------------- #

@require_POST
@customer_login_required
def get_complaint_form(request):
    return JsonResponse({
        utils.KEY_STATUS: utils.STATUS_OKAY,
        utils.KEY_FORM: RegisterComplaint()
    })


@require_POST
@customer_login_required
def process_complaint_form(request):
    form = RegisterComplaint(request.POST)
    if form.is_valid():
        c = Complaint.register_complaint(
            form.cleaned_data['oder_id'],
            form.cleaned_data['title'],
            form.cleaned_data['body']
        )
        return JsonResponse({
            utils.KEY_STATUS: utils.STATUS_OKAY,
            utils.KEY_COMPLAINT_NUMBER: c.id
        })
    return form_validation_error(form)
