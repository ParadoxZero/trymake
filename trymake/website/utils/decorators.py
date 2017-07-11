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

from trymake.apps.customer.models import Customer


def require_logged_out(func):
    def new_func(request):
        if request.user.is_authenticated():
            return HttpResponseForbidden()
        return func(request)

    return new_func
