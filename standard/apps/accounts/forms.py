from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from allauth.account.forms import SignupForm, LoginForm


class CustomUserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            if fieldname != "remember":
                field.widget.attrs.update({"class": "form-control form-control-lg"})


class CustomUserSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control form-control-lg"})

    def save(self, request):
        return super().save(request)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = "__all__"
        """ Should set up the fields to be seen explicitly
        (
            "email",
            "username",
            "first_name",
            "last_name",
            "address1",
            "address2",
            "address3",
            "address4",
            "terms_and_conditions",
        )
        """


class CustomUserPersonalDetailsUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            # "phone",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control form-control-lg"})


class CustomUserAddressDetailsUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = (
            "address1",
            "address2",
            "address3",
            "address4",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control form-control-lg"})


""" Remember to set these forms up appropriately for the project 
class CustomUserEmergencyContactUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = (
            "emergency_first_name",
            "emergency_last_name",
            "emergency_email",
            "emergency_phone",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control form-control-lg"})
"""