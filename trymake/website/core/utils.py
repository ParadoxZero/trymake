"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Trymake Inc
All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""
from django.http import HttpResponseRedirect


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

SESSION_CUSTOMER_ID = "customer_id"

KEY_STATUS = 'status'
KEY_ERROR_MESSAGE = 'error_message'
KEY_MESSAGE = 'message'
KEY_USER = "user"
KEY_LOGIN_FORM = "login_form"
KEY_REGISTRATION_FORM = "registration_form"
KEY_CHECK_EMAIL_FORM = "email_check_form"
KEY_FORM = "form"

KEY_EMAIL_REGISTERED = 'email_registered'

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
ERROR_INVALID_ADDRESS = "Input for address was invalid."


def redirect_to_origin(request):
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def get_context(request):
    return {
        KEY_USER: request.user if request.user.is_authenticated() else None,
    }
