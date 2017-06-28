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


def customer_login_required(func):
    def new_func(request):
        if request.user.is_authenticated():
            if request.user.groups.filter(name=Customer.GROUP_NAME).exists():
                return func(request)
        return HttpResponseForbidden()

    return new_func
