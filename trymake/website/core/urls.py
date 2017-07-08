"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

from django.conf.urls import url, include
from django.views.generic import TemplateView

from trymake.website.core import views

# NAMESPACE "core:account"
my_account_urls = [
    # Template
    url(r'^$', views.my_account, name="myaccount"),

    # AJAX views
    url(r'^ajax/orders/get$',views.get_order_list, name="get_order_list"),
    url(r'^ajax/orders/cancel$', views.cancel_order, name="cancel_order"),
    url(r'^ajax/order/return$', views.return_order, name="return_order"),
    # TODO delivery details
    url(r'^ajax/address/get$', views.get_address_list, name="get_address_list"),

    # Update profile
    url(r'^form/update/edit$' , views.get_update_profile_form , name="update_profile_edit"),
    url(r'^form/update/submit$', views.update_customer_profile, name="update_profile_submit"),

    # Feedback form
    url(r'^form/feedback/get$', views.get_feedback_form, name="get_feedback_form"),
    url(r'^form/feedback/submit$', views.process_feedback, name="submit_feedback_form"),

    # Address Form
    url(r'^form/address/get$', views.get_address_form, name="get_address_form"),
    url(r'^form/address/submit$', views.process_address_add, name="submit_address"),
    url(r'^form/address/edit$', views.edit_address, name="edit_address"),

    # Product Feedback Form
    url(r'^form/product_feedback/get$', views.get_product_feedback_form, name="get_product_feedback_form"),
    url(r'^form/product/submit/(?P<product_id>[0-9]+)', views.process_product_feedback, name="submit_product_feedback"),

    # Order Feedback Form
    url(r'^form/order_feedback/get', views.get_order_feedback_form, name="get_order_feedback"),
    url(r'^form/order_feedback/submit/(?P<order_id>[0-9]+)', views.process_order_feedback, name="process_order_feedback"),

]


# NAMESPACE "core"
urlpatterns = [
    # Template
    url(r'^$', views.index, name="index"),

    # LOGIN views - Core url namespace
    # AJAX views
    url(r'^authenticated$', views.is_Logged_in, name="authenticated"),
    url(r'^check_account$', views.check_account_exists, name="check_account"),
    url(r'^process_registration', views.process_registration , name="process_registration"),
    url(r'^register$', views.process_registration, name="reg"),

    # Redirect view
    url(r'logout$', views.logout_view, name="logout"),
    url(r'^login$', views.process_login, name="login"),
    url(r'^verify', views.process_email_verification, name="process_email_verification"),

    # ACCOUNT views - core:account url namespace
    url(r'^account/', include(my_account_urls, namespace="account")),

]
