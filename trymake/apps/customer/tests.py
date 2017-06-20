from django.test import TestCase
from django.urls import reverse

from trymakeAPI.API_1_0.mod_customer.models import Customer


class CustomerCreateTest(TestCase):

    def test_create_customer_no_group(self):
        Customer.create("sidhin","me@sidhin.in","sidhin1234","Sidhin","Thomas")
        try:
            sidhin = Customer.objects.get(user__username="sidhin")
        except Customer.DoesNotExist:
            sidhin = None
        print(sidhin.user.username)
        self.assertIsNotNone(sidhin)

    def test_api_create_customer(self):
        url = reverse("API_1_1:customer:create")
        print(url)
        response = self.client.post(reverse("API_1_1:customer:create"),{"username":"sidhin",
                                                                        "password":"sidhin",
                                                                        "first_name":"sidhin",
                                                                        "last_name":"thomas",
                                                                        "email":"me@sidhin.in"})
        self.assertContains(response,"ok")