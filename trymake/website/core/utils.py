#
#   Created by Sidhin S Thomas
#   Date: 28/06/17
#   
#   Copyright (C) 2017 www.trymake.com
#
from django.http import HttpResponseRedirect

from website.core.forms import LoginForm, RegistrationForm

###########################
# Error Messages ##########
###########################

INCORRECT_CREDENTIALS = "Incorrect username or password"
INVALID_INPUT = "Invalid Input"

############################
# Constants ################
############################

ERROR_MESSAGE = 'error_message'
MESSAGE = 'message'
LOGIN_FORM = "login_form"
REGISTRATION_FORM = "registration_form"
USER = "user"
LOGIN_FORM_DATA = "login_form_data"
REGISTRATION_FORM_DATA = "registration_form_data"


def redirect_to_origin(request):
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def get_context(request):
    return {
        MESSAGE: request.session.pop(MESSAGE, None),
        ERROR_MESSAGE: request.session.pop(ERROR_MESSAGE, None),
        LOGIN_FORM: LoginForm(request.session.get(LOGIN_FORM_DATA)),
        REGISTRATION_FORM: RegistrationForm(request.session.get(REGISTRATION_FORM_DATA)),
        USER: request.user if request.user.is_authenticated() else None,
    }
