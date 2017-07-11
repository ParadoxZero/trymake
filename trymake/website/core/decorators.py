"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.urls import reverse

from trymake.website import utils
from trymake.apps.customer.models import Customer
from trymake.website.utils import redirect_to_origin


def customer_login_required(func):
    def new_func(request):
        if request.user.is_authenticated():
            if request.user.groups.filter(name=Customer.GROUP_NAME).exists():
                user = request.user
                if not user.is_active:
                    request.session[utils.KEY_ERROR_MESSAGE] = utils.ERROR_VERIFY_EMAIL
                    request.sesssion[utils.KEY_SHOW_LOGIN] = True
                    return redirect_to_origin(request)
                return func(request)
        request.session[utils.KEY_ERROR_MESSAGE] = utils.ERROR_LOGIN_REQUIRED
        request.session[utils.KEY_SHOW_LOGIN] = True
        return redirect_to_origin(request)

    return new_func
