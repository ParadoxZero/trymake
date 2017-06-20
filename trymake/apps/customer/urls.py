from django.conf.urls import url

from trymakeAPI.API_1_0.mod_customer.views import AllCustomerView, CreateCustomer

urlpatterns = [
    url(r'^all/$',AllCustomerView.as_view(),name="all"),
    url(r'^create/',CreateCustomer.as_view(), name="create")
]