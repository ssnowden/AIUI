import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# from django.contrib.auth.models import Group
# from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    """
    If there are a number of different types of user, then break out
    these user types into 'Profile' models.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

    address1 = models.CharField(max_length=150, blank=True)
    address2 = models.CharField(max_length=150, blank=True)
    address3 = models.CharField(max_length=150, blank=True)
    address4 = models.CharField(max_length=150, blank=True)

    terms_and_conditions = models.BooleanField(
        default=False,
    )

    """ Set up appropriate fields for the user examples below. 
    staff_number = models.CharField(max_length=10, blank=True)
    emergency_first_name = models.CharField(
        max_length=150, blank=True, verbose_name=_("Contact first name")
    )
    emergency_last_name = models.CharField(
        max_length=150, blank=True, verbose_name=_("Contact last name")
    )
    emergency_email = models.EmailField(blank=True, verbose_name=_("Contact email"))

    # error message when a wrong format entered for phones
    phone_message = _("Phone number must be entered in the format: +44 7800 000 000")
    # desired format for phone numbers
    phone_regex = RegexValidator(
        regex=r"^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$",
        message=phone_message,
    )

    # finally, the phone number fields
    phone = models.CharField(validators=[phone_regex], max_length=60, null=True, blank=True)
    emergency_phone = models.CharField(
        validators=[phone_regex],
        max_length=60,
        null=True,
        blank=True,
        verbose_name=_("Contact phone number"),
    )
    """

    class Meta:
        verbose_name = _("A User")
        verbose_name_plural = _("Users")

    def get_absolute_url(self):
        return reverse("profile_detail", args=[self.uuid])
