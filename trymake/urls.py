"""trymake URL Configuration

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""

from django.conf.urls import url, include, static
from django.contrib import admin


# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/1.11/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.conf.urls import url, include
#     2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
from trymake import settings

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^vendor/', include('trymake.website.vendor.urls', namespace='vendor')),
    url(r'', include('trymake.website.core.urls', namespace="core")),
]

