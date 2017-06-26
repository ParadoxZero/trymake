from django.conf.urls import url

from trymake.website.core.views import index, process_login, process_registration, logout_view

urlpatterns = [
    url(r'^$', index, name="index" ),
    url(r'^login', process_login, name="login"),
    url(r'^reg', process_registration, name="reg"),
    url(r'logout', logout_view, name="logout"),
]