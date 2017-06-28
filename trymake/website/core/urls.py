from django.conf.urls import url, include

from trymake.website.core import views
my_account_urls = [
    url(r'^$', views.my_account, name="myaccount")
]


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login', views.process_login, name="login"),
    url(r'^register', views.process_registration, name="reg"),
    url(r'logout', views.logout_view, name="logout"),
    url(r'^account/', include(my_account_urls, namespace="account"))
]