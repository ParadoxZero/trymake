"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

from django.http import HttpResponseRedirect, JsonResponse

#################################################################################
# CONSTANTS                                                                     #
# ----------------------------------------------------------------------------- #
# SESSION/CONTEXT keys                                                          #
#                                                                               #
#  1) SESSION_CUSTOMER_ID: id of logged in customer                             #
#  2) KEY_REGISTRATION_FORM_DATA: data of failed registration form              #
#  3) KEY_LOGIN_FORM_DATA: data of failed login form                            #
#  4) KEY_ADDRESS_FORM_DATA: data of failed address form                        #
#  5) KEY_ERROR_MESSAGE: error message to display in case                       #
#  6) KEY_MESSAGE: message to display                                           #
#  7) KEY_LOGIN_FORM                                                            #
#  8) KEY_REGISTRATION_FORM                                                     #
#  9) KEY_USER                                                                  #
#                                                                               #
# Constant Values                                                               #
#                                                                               #
#  1) STATUS_OKAY                                                               #
#  2) STATUS_ERROR                                                              #
#                                                                               #
# Error Messages                                                                #
#                                                                               #
#  1) INVALID ADDRESS                                                           #
#  2) ERROR_INVALID_INPUT: just for any arbitary error                          #
#  3) ERROR_INVALID_ADDRESS                                                     #
#################################################################################
from django.urls import reverse

from trymake.website.core.forms import LoginForm, RegistrationForm

SESSION_CUSTOMER_ID = 'customer_id'
SESSION_PAGE_DETAIL = 'page_details'
SESSION_OTP_SECRET = 'otp_secret'
SESSION_PHONE_NUMBER = 'phone_number'

KEY_STATUS = 'status'
KEY_ERROR_MESSAGE = 'error_message'
KEY_MESSAGE = 'message'
KEY_USER = 'user'
KEY_EMAIL = 'email'
KEY_NAME = 'name'
KEY_ADDRESS_NAME = 'address_name'
KEY_NUMBER = 'num'
KEY_ORDER_LIST = 'order_list'
KEY_ADDRESS_LIST = 'address_list'
KEY_COMPLAINT_NUMBER = 'complaint_number'
KEY_COMPLAINT = 'complaint'

# Processing entities
KEY_LOGIN_FORM = "login_form"
KEY_REGISTRATION_FORM = "registration_form"
KEY_CHECK_EMAIL_FORM = "email_check_form"
KEY_FORM = "form"

# Flags
KEY_EMAIL_REGISTERED = 'email_registered'
KEY_PHONE_REGISTERED = 'phone_registered'
KEY_IS_AUTHENTICATED = 'is_authenticated'
KEY_FINISHED = 'finished'
KEY_RETURN_ACCEPTED = 'return_accepted'
KEY_CANCEL_ACCEPTED = 'cancel_accepted'
KEY_SHOW_LOGIN = 'show_login'

###########################
# CONSTANT VALUES         #
###########################

STATUS_OKAY = 'ok'
STATUS_ERROR = 'error'

###########################
# Error Messages          #
###########################

ERROR_INCORRECT_CREDENTIALS = "Incorrect username or password"
ERROR_INVALID_INPUT = "Invalid Input"
ERROR_ADDRESS_NOT_FOUND = "No address found with the given name"
ERROR_ALREADY_EXISTS = "Already exists"
ERROR_MISSING_DATA = "Missing Data"
ERROR_CUSTOMER_DOES_NOT_EXISTS = "Requested customer does not exists"
ERROR_INVALID_TOKEN = "Invalid Token"
ERROR_VERIFY_EMAIL = "Please verify your email"
ERROR_LOGIN_REQUIRED = "You will need to Login to access that url"

###########################
# Messages                #
###########################

MESSAGE_VERIFICATION_SUCCESSFUL = "Email verification successful"


def redirect_to_origin(request) -> HttpResponseRedirect:
    url = request.META.get("HTTP_REFERER", reverse("core:index"))
    return HttpResponseRedirect(url)


def form_validation_error(form) -> JsonResponse:
    return JsonResponse({
        KEY_STATUS: STATUS_ERROR,
        KEY_ERROR_MESSAGE: ERROR_INVALID_INPUT,
        KEY_FORM: form.as_table()
    })


def get_template_context(request) -> dict:
    return {
        KEY_STATUS: request.session.pop(KEY_STATUS, STATUS_OKAY),
        KEY_MESSAGE: request.session.pop(KEY_MESSAGE, None),
        KEY_ERROR_MESSAGE: request.session.pop(KEY_ERROR_MESSAGE, None),
        KEY_LOGIN_FORM: request.session.pop(KEY_LOGIN_FORM, LoginForm()),
        KEY_REGISTRATION_FORM: request.session.pop(KEY_REGISTRATION_FORM, RegistrationForm()),
        KEY_USER: request.user,
        KEY_IS_AUTHENTICATED: request.user.is_authenticated(),
        KEY_SHOW_LOGIN: request.session.pop(KEY_SHOW_LOGIN,False)
    }
