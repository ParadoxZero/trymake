from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from trymake import settings
from trymake.apps.complaints.models import Complaint
from trymake.apps.customer.models import Customer
from trymake.apps.orders_management.models import Order

from trymake.website.core import utils
from trymake.website.core.forms import EnterEmailForm, RegistrationForm, LoginForm, AddressForm, FeedbackForm
from trymake.website.core.utils import get_context, ERROR_MESSAGE
from website.core.decorators import require_logged_out, customer_login_required

############################
# Constants ################
############################



###########################
# Error Messages ##########
###########################

INCORRECT_CREDENTIALS = "Incorrect username or password"
INVALID_INPUT = "Invalid Input"


def redirect_to_origin(request):
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
###########################


def index(request):
    context = {ERROR_MESSAGE: request.session.get('error_message', ""),
               'login_form': LoginForm(request.session.get('login_form_data')),
               'user': request.user if request.user.is_authenticated() is not None else "",
               'registration_form': RegistrationForm(request.session.get('registration_form_data')),
               'address_form': AddressForm()}
    request.session.pop('login_form_data', None)
    request.session.pop('registration_form_data', None)
    request.session.pop('error_message', None)
    print()
    return render(request, 'website/core/index.html', context)


####################################################################################################################
# Login views                                                                                                      #
####################################################################################################################


#
# Trymake Login flow in four phases/parts:
#     1) user enters email
#     2) if email exists in database, show password field
#     3) email exists, but not verified, show resend verification link
#     4) if email doesn't exist, show registration field
#

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
    return JsonResponse({"status": "fail", "reason": INVALID_INPUT})


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
    else:
        request.session[ERROR_MESSAGE] = INCORRECT_CREDENTIALS
        if settings.DEBUG:
            print("Debug: ", form.errors)
        request.session[utils.LOGIN_FORM_DATA] = request.POST
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
        request.session[ERROR_MESSAGE] = INVALID_INPUT
        request.session[utils.REGISTRATION_FORM_DATA] = request.POST
    return redirect_to_origin(request)


def logout_view(request):
    logout(request)

    return HttpResponseRedirect("/")


####################################################################################################################
# Account Views                                                                                                    #
####################################################################################################################

@customer_login_required
def my_account(request):
    context = get_context(request)
    context['orders'] = Order.objects.filter(customer__user=request.user).order_by('-date_placed')[:3]
    context['customer'] = Customer.objects.get(user=request.user)
    context['complaints'] = Complaint.objects.filter(order__customer__user=request.user)
    return render(request,'website/core/my_account.html', context=context)


@customer_login_required
@require_POST
def process_feedback(request):
    form = FeedbackForm(request.POST)
    if form.is_valid():
        customer = Customer.objects.get(user=request.user)
        form.save_feedback(customer)
    else:
        request.session[ERROR_MESSAGE] = INVALID_INPUT
    return redirect_to_origin(request)



