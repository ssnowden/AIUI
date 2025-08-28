"""Admin configuration for the chats app.

This module defines how the chats app models appear and behave in the Django admin site.
It includes admin classes for conversation threads and their items, with customizations for
different thread types.
"""

from django.contrib import admin
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from .models import (
    APIConversationThread,
    ConversationItem,
    NOAConversationThread,
    WebConversationThread,
)


# Register your models here.
class ConversationItemInLine(admin.TabularInline):
    """Displays ConversationItem instances inline within a ConversationThread in the admin.

    Allows a list of ConversationItem model instances to be displayed as a table in a parent ConversationThread admin page.
    """

    model: type[ConversationItem] = ConversationItem


class ConversationThreadAdmin(admin.ModelAdmin):
    """Admin configuration for ConversationThread models.

    Provides inline display of conversation items and customizes the list display
    for conversation threads.
    """

    inlines: list[type[admin.TabularInline]] = [
        ConversationItemInLine,
    ]

    list_display: tuple[str, ...] = ("name", "summary")
    # For the create/update forms
    # fields: tuple[Any, ...] = (("field1", "field2"), "field3")

    # ...or use a field set to group fields under headings.

    # fieldsets: tuple[
    #     tuple[str, dict[str, Any]],
    #     ...
    # ] = (
    #     (
    #         "Title for a section1",
    #         {
    #             "fields": ("field1",),
    #             "description": _("Some descriptive text for this section"),
    #         },
    #     ),
    #     (
    #         "Title for a section2",
    #         {
    #             "classes": ("collapse",),
    #             "fields": ("field2", "field3"),
    #             "description": _("Some descriptive text for this section. With collapse set, click show to see."),
    #         },
    #     ),
    # )


class WebConversationThreadAdmin(ConversationThreadAdmin):
    """Admin configuration for WebConversationThread models.

    Filters the queryset to only include threads of type 'web'.
    """

    def get_queryset(self, request) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.filter(chat_type="web")


class NOAConversationThreadAdmin(ConversationThreadAdmin):
    """Admin configuration for NOAConversationThread models.

    Filters the queryset to only include threads of type 'noa'.
    """

    def get_queryset(self, request) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.filter(chat_type="noa")


class APIConversationThreadAdmin(ConversationThreadAdmin):
    """Admin configuration for APIConversationThread models.

    Filters the queryset to only include threads of type 'api'.
    """

    def get_queryset(self, request) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.filter(chat_type="api")


admin.site.register(WebConversationThread, WebConversationThreadAdmin)
admin.site.register(NOAConversationThread, NOAConversationThreadAdmin)
admin.site.register(APIConversationThread, APIConversationThreadAdmin)
