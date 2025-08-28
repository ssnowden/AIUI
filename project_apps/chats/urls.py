"""This module provides the URLs for the conversationthreadss app.

It has the URLs:
    BASE URL: "procedures/".

    conversationthreads: URL name to show a list of the ConversationThreads model instances: BASE URL ONLY.

    conversationthread_detail: URL name to show the detail of a ConversationThreads model instance: BASE URL + INSTANCE ID/.

    conversationthread_create: URL name to create a list of the ConversationThreads model instance: BASE URL + create/ + INSTANCE ID/.

    conversation_thread_delete: URL name to delete a list of the ConversationThreads model instance: BASE URL + delete/ + INSTANCE ID/.

    API endpoints
    send_prompt_with_id: send a prompt with a specific ConversationThreads ID
    send_prompt: send a prompt without a specific ConversationThreads ID (creates a new ConversationThreads)
"""

from django.urls import include, path

from .views import (
    ConversationThreadCreateView,
    ConversationThreadDeleteView,
    ConversationThreadDetailView,
    ConversationThreadListView,
    send_prompt,
)

urlpatterns = [
    path("", ConversationThreadListView.as_view(), name="conversationthreads"),
    path(
        "<uuid:pk>/",
        ConversationThreadDetailView.as_view(),
        name="conversationthread_detail",
    ),
    path(
        "create/",
        ConversationThreadCreateView.as_view(),
        name="conversationthread_create",
    ),
    path(
        "delete/<uuid:pk>/",
        ConversationThreadDeleteView.as_view(),
        name="conversation_thread_delete",
    ),
    # Include API endpoints
    path("send_prompt/<uuid:thread_id>", send_prompt, name="send_prompt_with_id"),
    path("send_prompt/", send_prompt, name="send_prompt"),
]
