from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render

from trymake import settings
from trymake.apps.customer.models import Customer
from trymake.website.ecommerce.forms import EnterEmailForm, RegistrationForm, LoginForm

###########################
# Error Messages ##########
###########################


INCORRECT_CREDENTIALS = "Incorrect username or password"
INVALID_INPUT = "Invalid Input"


################################################################################################
# Login views
################################################################################################


#
# Trymake Login flow in four phases/parts:
#     1) user enters email
#     2) if email exists in database, show password field
#     3) email exists, but not verified, show resend verification link
#     4) if email doesn't exist, show registration field
#


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


def process_login(request):
    """
    Login phase two when email exists
    """
    if request.method != "POST":  # If reached incorrectly
        return HttpResponseNotAllowed(permitted_methods=["POST"])
    form = LoginForm(request.POST)
    if form.is_valid():
        user = form.cleaned_data['user']
        login(request, user)
    else:
        request.session['error_message'] = INCORRECT_CREDENTIALS
        if True:
            print(form.errors)
        request.session['login_form'] = request.POST
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def process_registration(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])
    form = RegistrationForm(request.POST)
    if form.is_valid():
        customer = Customer.create(
            email=form.cleaned_data.get("email"),
            phone=str(form.cleaned_data.get("phone")),
            password=str(form.cleaned_data.get("password")),
            firstname=form.cleaned_data.get("name")
        )
    else:
        request.session['error_message'] = INVALID_INPUT
        request.session['registration_form'] = request.POST
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def index(request):
    context = {'error_message': request.session.get('error_message', ""),
               'login_form': LoginForm(request.session.get('login_form')),
               'registration_form': RegistrationForm(request.session.get('registration_form'))}
    request.session.pop('login_form', None)
    request.session.pop('registration_form', None)
    request.session.pop('error_message', None)
    return render(request, 'website/ecommerce/index.html', context)
