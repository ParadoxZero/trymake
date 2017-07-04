"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
from django.conf.urls import url

from trymake.website.vendor import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^product_add/submit$', views.product_add, name="product_add"),
    url(r'^additional_image_add/submit/(?P<product_slug>[\w]{1,10})', views.image_add, name="additional_image_add")
]
