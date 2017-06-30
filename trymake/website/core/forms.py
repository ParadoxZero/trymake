"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Trymake Inc
All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from trymake.apps.orders_management.models import Order
from trymake.apps.user_interactions.models import Feedback, OrderFeedback, ProductFeedback
from trymake.apps.customer.models import State, Customer
from trymake.website.core.validators import email_doesnt_exist, pin_validator, phone_validator, phone_doesnt_exist


class EnterEmailForm(forms.Form):
    email = forms.EmailField(
        label="Enter Email",
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': "Enter Email"
        }),
    )


class LoginForm(forms.Form):
    ERROR_MESSAGES = {
        "invalid_login":"Invalid credentials"
    }

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'autofocus': True,
                'placeholder': "Email"
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': "Password"
            }
        ),
    )

    remember_me = forms.BooleanField(
        label="Remember me?",
        initial=True,
        required=False
    )

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user = None
        self.customer_id = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user = authenticate(self.request, username=username, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    self.ERROR_MESSAGES['invalid_login'],
                    code='invalid_login',
                )
            try:
                customer = Customer.objects.get(user=self.user)
            except Customer.DoesNotExist:
                raise forms.ValidationError(
                    self.ERROR_MESSAGES['invalid_login'],
                    code='invalid_login',
                )
            self.customer_id = customer.id
        return self.cleaned_data


class RegistrationForm(forms.Form):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={
            'autofocus': True,
            "placeholder": "Enter Name"
        })
    )

    phone = forms.CharField(
        label="Phone",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter Phone Number"
        }),
        validators=[phone_validator, phone_doesnt_exist]
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Email"
            }),
        validators=[email_doesnt_exist]
    )

    password = forms.CharField(
        label="Password",
        help_text="Make sure to enter long password",
        strip=False,
        widget=forms.PasswordInput,
    )

    password_verify = forms.CharField(
        label="Repeat Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean_password_verify(self):
        password = self.cleaned_data.get("password")
        password_verify = self.cleaned_data.get("password_verify")
        if password and password_verify:
            if password != password_verify:
                raise ValidationError("Passwords don't match", code="password_mismatch")
        validate_password(password)
        return password_verify


class AddressForm(forms.Form):
    name = forms.CharField(max_length=255)
    phone = forms.CharField(validators=[phone_validator], max_length=11)

    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'autofocus': True,
        }),
    )
    pincode = forms.CharField(max_length=6, validators=[pin_validator])

    landmark = forms.CharField()
    city = forms.CharField()
    state = forms.ModelChoiceField(queryset=State.objects.filter(country__code='IN'))


class UpdateProfileForm(forms.Form):
    name = forms.CharField()
    phone = forms.CharField(validators=[phone_validator], max_length=11)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Current Password",
        help_text="Enter Current Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    password1 = forms.CharField(
        label="New Password",
        help_text="Make sure to enter long password",
        strip=False,
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label="Repeat Password",
        help_text="Enter your new password again",
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean_password2(self):
        password = self.cleaned_data.get("password1")
        password_verify = self.cleaned_data.get("password2")
        if password and password_verify:
            if password != password_verify:
                raise ValidationError("Passwords don't match", code="password_mismatch")
        validate_password(password_verify)
        return password_verify


class ProductFeedbackForm(forms.ModelForm):
    class Meta:
        model = ProductFeedback
        exclude = ['verified_buyer', 'customer']

    def save_feedback(self, customer: Customer):
        """
            Feedback needs option which customer is saving.
        :type customer: Customer
        """
        self.instance.customer = customer
        return self.save()


class OrderFeedbackForm(forms.ModelForm):
    class Meta:
        model = OrderFeedback
        exclude = ['order']

    def save_feedback(self, order: Order):
        self.instance.order = order
        return self.save()


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ['customer']

    def save_feedback(self, customer: Customer):
        """
            Feedback needs which customer is saving.
        :type customer: Customer
        """
        self.instance.customer = customer
        return self.save()


class RegisterComplaint(forms.Form):
    oder_id = forms.CharField(max_length=6)
    title = forms.CharField(max_length=140)
    body = forms.CharField(
        widget=forms.Textarea
    )

