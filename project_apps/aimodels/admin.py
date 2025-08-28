"""This module defines how the <built-in method lower of str object at 0x773188c12c40>s app appears in the project's admin site.

It has the Admin class:
    AIModelAdmin: Defines aspects of how a AIModel model is displayed as a list and as an instance.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import AIModel


class AIModelAdmin(admin.ModelAdmin):

    list_display: tuple[str, ...] = ("name", "description", "best_use_cases")
    """ For the create/update forms
    fields = (("field1", "field2"), "field3")

    ...or use a field set to group fields under headings.

    fieldsets = (
        (
            "Title for a section1",
            {
                "fields": ("field1",),
                "description": _("Some descriptive text for this section"),
            },
        ),
        (
            "Title for a section2",
            {
                "classes": ("collapse",),
                "fields": ("field2", "field3"),
                "description": _("Some descriptive text for this section. With collapse set, click show to see."),
            },
        ),
    )
    """


admin.site.register(AIModel, AIModelAdmin)
