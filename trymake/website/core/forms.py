from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from trymake.website.core.validators import validator_email_doesnt_exist


class EnterEmailForm(forms.Form):
    email = forms.EmailField(
        label="Enter Email",
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': "Enter Email"
        }),
        validators=[validator_email_doesnt_exist]
    )


class LoginForm(forms.Form):
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
        initial=True
    )

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user = authenticate(self.request, username=username, password=password)
            if self.user is None:
                self.add_error(
                    password,
                    forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )
                )
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        return self.cleaned_data


class RegistrationForm(forms.Form):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={
            'autofocus': True,
            "placeholder": "Enter Name"})
    )

    phone = forms.CharField(
        label="Phone",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter Phone Number"
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Email"
            }),
        validators=[validator_email_doesnt_exist]
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
