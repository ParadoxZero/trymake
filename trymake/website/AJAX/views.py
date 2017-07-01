""" Views that are purely AJAX i.e. NOT involving any form processing

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET

from trymake.apps.orders_management.models import Order
from trymake.website import utils
from trymake.website.utils.decorators import require_logged_out,customer_login_required


@require_GET
@customer_login_required
def get_orders(request):
    number = request.GET[utils.KEY_NUMBER]
    orders = Order.objects.filter(customer_id=request.session[utils.SESSION_CUSTOMER_ID])[:number]
