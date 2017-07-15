"""

Author: Sidhin S Thomas (sidhin@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

"""
import uuid

import pyotp
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from trymake.apps.customer.models import State, Customer
from trymake.apps.user_interactions.models import Feedback, OrderFeedback, ProductFeedback
from trymake.website.core.validators import email_doesnt_exist, pin_validator, phone_validator, phone_doesnt_exist, \
    otp_validator


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
        "invalid_login": "Invalid credentials"
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
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'ng-model': "name"
        })
    )
    phone = forms.CharField(
        validators=[phone_validator],
        max_length=11,
        widget=forms.TextInput(attrs={
            'ng-model': "phone"
        })
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'ng-model': "address"
        }),
    )
    pincode = forms.CharField(
        max_length=6,
        validators=[pin_validator],
        widget=forms.TextInput(attrs={
            'ng-model': "pincode"
        })
    )

    landmark = forms.CharField(
        widget=forms.TextInput(attrs={
            'ng-model': "landmark"
        })
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={
            'ng-model': "city"
        })
    )
    state = forms.ModelChoiceField(
        queryset=State.objects.filter(country__code='IN'),
        widget=forms.Select(attrs={'ng-model': "state"}))


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


class ResetPasswordForm(forms.Form):
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
        exclude = ['verified_buyer', 'customer', 'product']

    def save_feedback(self, customer: str, product: int):
        """
            Feedback needs option which customer is saving.
        """
        self.instance.customer_id = uuid.UUID(customer)
        self.instance.product_id = product
        return self.save()


class OrderFeedbackForm(forms.ModelForm):
    class Meta:
        model = OrderFeedback
        exclude = ['order']

    def save_feedback(self, order_id: str):
        self.instance.order_id = order_id
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


class PhoneNumberForm(forms.Form):
    phone = forms.CharField(validators=[phone_validator, phone_doesnt_exist], max_length=11)


class PhoneOTPForm(forms.Form):
    otp = forms.CharField(validators=[otp_validator], max_length=6)

    def __init__(self, secret=None, *args, **kwargs):
        self.otp_secret = secret
        super(PhoneOTPForm, self).__init__(*args, **kwargs)


    def clean(self):
        otp = pyotp.TOTP(self.otp_secret)
        if not otp.verify(self.cleaned_data['otp'], valid_window=settings.OTP_VALID_DURATION):
            raise ValidationError(message="Invalid OTP", code="invalid")
        return self.cleaned_data

