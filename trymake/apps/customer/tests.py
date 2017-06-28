"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Trymake Inc
All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from trymake.apps.customer.models import Customer, Country, State, Address


class CustomerTest(TestCase):
    def setUp(self):
        c = Country()
        c.name = "India"
        c.save()
        s = State()
        s.name = "Delhi"
        s.country = c
        s.save()

    def test_create_customer_no_group(self):
        try:
            Customer.create("me@sidhin.in", "sidhin1234", "Sidhin", "Thomas")
            sidhin = Customer.objects.get(user__username="me@sidhin.in")
        except Customer.DoesNotExist:
            sidhin = None
        self.assertIsNotNone(sidhin)

    def test_create_customer_repeated_email(self):
        Customer.create("me@sidhin.in", "sidhin1234", "Sidhin", "Thomas")
        try:
            Customer.create("me@sidhin.in", "sidhin1234", "Sidhin", "Thomas")
            value = True
        except IntegrityError:
            value = False
        self.assertIs(value,False)

    def test_set_address(self):
        sidhin=Customer.create("me@sidhin.in","sidhin1234","Sidhin","Thomas")
        sidhin.add_address("test_addr","Long address","New Delhi",
                           State.objects.get(name="Delhi"),"110075","Mtro station","9447480852")
        address = Address.objects.filter(customer=sidhin)
        self.assertEqual(address.count(),1)

    def test_get_address(self):
        sidhin = Customer.create("me@sidhin.in","sidhin1234","Sidhin","Thomas")
        sidhin.add_address("test_addr", "Long address", "New Delhi",
                           State.objects.get(name="Delhi"), "110075", "Mtro station", "9447480852")
        list = sidhin.get_address_list()
        self.assertEqual(list.count(),1)
        addresss = list.first()
        self.assertEqual(addresss.name,"test_addr")