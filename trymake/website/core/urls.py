"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

from django.conf.urls import url, include

from trymake.website.core import views

# NAMESPACE "core:account"
my_account_urls = [
    url(r'^$', views.my_account, name="myaccount"),
    # AJAX views
    # Feedback form
    url(r'^form/feedback/get$', views.get_feedback_form, name="get_feedback_form"),
    url(r'^form/feedback/submit$', views.process_feedback, name="submit_feedback_form"),

    # AJAX views
    # Address Form
    url(r'^form/address/get$', views.get_address_form, name="get_address_form"),
    url(r'^form/address/submit$', views.process_address_add, name="submit_address"),
    url(r'^form/address/edit$', views.edit_address, name="edit_address")
]


# NAMESPACE "core"
urlpatterns = [
    url(r'^$', views.index, name="index"),

    # LOGIN views - Core url namespace
    # AJAX views
    url(r'^authenticated$', views.is_Logged_in, name="authenticated"),
    url(r'^check_account$', views.check_account_exists, name="check_account"),
    url(r'^process_registration', views.process_registration , name="process_registration"),
    url(r'^login$', views.process_login, name="login"),
    url(r'^register$', views.process_registration, name="reg"),

    # Redirect view
    url(r'logout$', views.logout_view, name="logout"),

    # ACCOUNT views - core:account url namespace
    url(r'^account/', include(my_account_urls, namespace="account"))
]
