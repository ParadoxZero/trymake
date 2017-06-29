"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Trymake Inc
All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""
from django.http import HttpResponseRedirect

from trymake.website.core.forms import LoginForm, RegistrationForm

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
#                                                                               #
# Error Messages                                                                #
#                                                                               #
#  1) INVALID ADDRESS                                                           #
#  2) ERROR_INVALID_INPUT: just for any arbitary error                          #
#  3) ERROR_INVALID_ADDRESS                                                     #
#################################################################################

SESSION_CUSTOMER_ID = "customer_id"
KEY_REGISTRATION_FORM_DATA = "registration_form_data"
KEY_LOGIN_FORM_DATA = "login_form_data"
KEY_ADDRESS_FORM_DATA = "address_form_data"
KEY_ERROR_MESSAGE = 'error_message'
KEY_MESSAGE = 'message'
KEY_LOGIN_FORM = "login_form"
KEY_REGISTRATION_FORM = "registration_form"
KEY_USER = "user"

###########################
# Error Messages          #
###########################

ERROR_INCORRECT_CREDENTIALS = "Incorrect username or password"
ERROR_INVALID_INPUT = "Invalid Input"
ERROR_INVALID_ADDRESS = "Input for address was invalid."


def redirect_to_origin(request):
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def get_context(request):
    return {
        KEY_MESSAGE: request.session.pop(KEY_MESSAGE, None),
        KEY_ERROR_MESSAGE: request.session.pop(KEY_ERROR_MESSAGE, None),
        KEY_LOGIN_FORM: LoginForm(request.session.pop(KEY_LOGIN_FORM_DATA, None)),
        KEY_REGISTRATION_FORM: RegistrationForm(request.session.pop(KEY_REGISTRATION_FORM_DATA, None)),
        KEY_USER: request.user if request.user.is_authenticated() else None,
    }
