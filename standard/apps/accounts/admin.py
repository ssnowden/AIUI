from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    """ Set up the items that will be displayed in admin list for accounts 
    list_display = [
        "email",
        "phone",
        "is_staff",
        "is_superuser",
    ]
    """
    """ Set up the field sets for the user detailed view in admin 
    fieldsets = (
        (
            ("Personal"),
            {
                "fields": (
                    "email",
                    "staff_number",
                    "password",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "terms_and_conditions",
                )
            },
        ),
        (
            ("Contact Details"),
            {
                "fields": (
                    "phone",
                    "address1",
                    "address2",
                    "address3",
                    "address4",
                )
            },
        ),
        (
            ("Roles and Permissions"),
            {
                "fields": (
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            ("Emergency Contact Details"),
            {
                "fields": (
                    "emergency_first_name",
                    "emergency_last_name",
                    "emergency_email",
                    "emergency_phone",
                )
            },
        ),
    )
    """


admin.site.register(CustomUser, CustomUserAdmin)