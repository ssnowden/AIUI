"""project_apps.chats.models.py

Description of the models.

class ConversationThread(models.Model)
    - The base model for the app.
    - fields
        id
        name
        summary
        aimodel
        chat_type
        created_by
        created_at
        modified_by
        modified_at
    - str representation:
    - get_absolute_url:

class ConversationItem(models.Model)
    - The multi-item model for the base model.
    - fields
        id
        conversation_thread
        prompt
        response
        tokens
        is_full_saved
        created_by
        created_at
        modified_by
        modified_at
        ORDER
    - str representation:
    - get_absolute_url: conversationthread_detail/parent_model_id


"""

import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from project_apps.aimodels.models import AIModel

# from django_cryptography.fields import encrypt # Removed due to incompatibility with Django 5


class ConversationThread(models.Model):
    """Represents a thread of conversation between users and AI models.

    This model stores metadata about a conversation, including its type,
    associated AI model, and creator/modifier information.
    """

    THREAD_TYPES: list[tuple[str, str]] = [
        ("web", "Web"),
        ("api", "API"),
        ("noa", "NOA"),
    ]
    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name: models.CharField = models.CharField(
        max_length=150, blank=False, null=False, verbose_name="Conversation Name"
    )

    summary: models.TextField = models.TextField(
        blank=True, null=True, verbose_name="Conversation Summary"
    )

    aimodel: models.ForeignKey = models.ForeignKey(
        AIModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="conversation_models",
        verbose_name=_("Conversation AI Models"),
    )

    chat_type: models.CharField = models.CharField(
        max_length=150,
        default="web",
        blank=False,
        null=False,
        verbose_name=_("Conversation Type"),
        choices=THREAD_TYPES,
    )

    created_by: models.ForeignKey = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_lists",
        verbose_name=_("Conversation Created By"),
    )
    created_at: models.DateField = models.DateField(
        auto_now_add=True, verbose_name="Conversation Created At"
    )
    modified_by: models.ForeignKey = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="modified_lists",
        verbose_name=_("Conversation Modified By"),
    )
    modified_at: models.DateField = models.DateField(
        auto_now=True, verbose_name="Conversation Modified At"
    )

    class Meta:
        """Meta options for ConversationThread.

        Sets verbose names for the admin interface.
        """

        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")

    def __str__(self) -> str:
        """Returns the string representation of the conversation thread.

        Returns:
            str: The name of the conversation thread.
        """

        return self.name

    def get_absolute_url(self) -> str:
        """Returns the absolute URL for the conversation thread detail view.

        Returns:
            str: The URL for the conversation thread detail page.
        """
        return reverse("conversationthread_detail", args=[self.id])


class WebConversationThread(ConversationThread):
    class Meta:
        proxy: bool = True
        verbose_name: str = _("Web Conversation")
        verbose_name_plural: str = _("Web Conversations")


class NOAConversationThread(ConversationThread):
    class Meta:
        proxy: bool = True
        verbose_name: str = _("NOA Conversation")
        verbose_name_plural: str = _("NOA Conversations")


class APIConversationThread(ConversationThread):
    class Meta:
        proxy: bool = True
        verbose_name: str = _("API Conversation")
        verbose_name_plural: str = _("API Conversations")


class ConversationItem(models.Model):
    """Represents an item in a conversation thread.

    This model stores individual prompt-response pairs within a conversation thread,
    along with metadata such as token usage and creator/modifier information.
    """

    id: models.UUIDField = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    conversation_thread: models.ForeignKey = models.ForeignKey(
        ConversationThread,
        on_delete=models.CASCADE,
        null=False,
        related_name="conversation_items",
        verbose_name=_("Conversation Items"),
    )
    prompt: models.TextField = models.TextField(
        blank=False, null=False, verbose_name=_("Conversation's Item's Prompt")
    )
    response: models.TextField = models.TextField(
        blank=False, null=False, verbose_name=_("Conversation's Item's Response")
    )

    tokens: models.IntegerField = models.IntegerField()
    is_full_saved: models.BooleanField = models.BooleanField(default=False)
    created_by: models.ForeignKey = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_conversation_items",
        verbose_name=_("Chats Item Created By"),
    )
    created_at: models.DateField = models.DateField(
        auto_now_add=True, verbose_name=_("Chats Item Created At")
    )
    modified_by: models.ForeignKey = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name="modified_conversation_items",
        verbose_name=_("Chats Item Modified By"),
    )
    modified_at: models.DateField = models.DateField(
        auto_now=True, verbose_name=_("Chats Item Modified At")
    )
    ORDER: models.IntegerField = models.IntegerField(
        default=0, blank=True, null=True, verbose_name=_("Order in Chats")
    )

    class Meta:
        """Meta options for ConversationItem.

        Sets ordering for lists of items and verbose names for the admin interface.
        """

        ordering = ["ORDER"]

        verbose_name = _("Conversation Item")
        verbose_name_plural = _("Conversation Items")

    def __str__(self) -> str:
        """Returns the string representation of the conversation item.

        Returns:
            str: A description of the conversation item including chat name,
            creator, modifier, and token usage.
        """
        return str(
            _(
                f"Item for chat {self.conversation_thread.name} created by {self.created_by}, modified by {self.modified_by} and used {self.tokens} tokens"
            )
        )

    def get_absolute_url(self) -> str:
        """Returns the absolute URL for the parent conversation thread detail view.

        Returns:
            str: The URL for the parent conversation thread detail page.
        """
        return reverse("conversationthread_detail", args=[self.conversation_thread.id])
