from django.test import TestCase
from django.urls import reverse

from trymake.apps.customer.models import Customer, Country, State, Address


class CustomerTest(TestCase):
    def setUp(self):
        Customer.create("sidhin","me@sidhin.in","sidhin1234","Sidhin","Thomas")
        c = Country()
        c.name = "India"
        c.save()
        s = State()
        s.name = "Delhi"
        s.country = c
        s.save()

    def test_create_customer_no_group(self):
        try:
            sidhin = Customer.objects.get(user__username="sidhin")
        except Customer.DoesNotExist:
            sidhin = None
        self.assertIsNotNone(sidhin)

    def test_set_address(self):
        sidhin = Customer.objects.get(user__username="sidhin")
        sidhin.add_address("test_addr","Long address","New Delhi",
                           State.objects.get(name="Delhi"),"110075","Mtro station","9447480852")
        address = Address.objects.filter(customer=sidhin)
        self.assertEqual(address.count(),1)

    def test_get_address(self):
        sidhin = Customer.objects.get(user__username="sidhin")
        sidhin.add_address("test_addr", "Long address", "New Delhi",
                           State.objects.get(name="Delhi"), "110075", "Mtro station", "9447480852")
        list = sidhin.get_address_list()
        self.assertEqual(list.count(),1)
        addresss = list.first()
        self.assertEqual(addresss.name,"test_addr")