"""project_apps.chats.views.py
This module provides the views for the conversationthreads app accessed by the URLs.

    Description for the views.

    --------- Base setup of views --------------
    class ChatsListView(LoginRequiredMixin, ListView):
        - Shows a list for chats

    class ChatsDetailView(LoginRequiredMixin, DetailView):
        - Shows a detail view for chat

    ---------- Edit views -------------
    class ChatsCreateView(LoginRequiredMixin, CreateView):
        - Create view for chat

    class ChatsDeleteView(LoginRequiredMixin, DeleteView):
        - Delete view for chat
"""

import logging
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import QuerySet
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView

from standard.views.mixins import ProjectNameMixin

from .forms import ConversationItemForm, ConversationThreadForm
from .models import ConversationItem, ConversationThread

logger = logging.getLogger(__name__)


class ConversationThreadViewPermissionTestMixin:
    def test_func(self) -> bool:
        """This will need an appropriate test for views."""
        # This is part of the test for Anonymous users.
        if not self.request.user.id:
            return False
        try:
            return True
        except Exception:
            return False


class ConversationThreadListView(ProjectNameMixin, LoginRequiredMixin, ListView):
    """List view for ConversationThread objects.

    Displays a list of conversation threads filtered by chat type for the authenticated user.
    """

    model = ConversationThread
    context_object_name = "conversation_threads"
    template_name = "chats/list/chats_list.html"

    def get_queryset(self) -> QuerySet[ConversationThread]:
        """Return a queryset of conversation threads filtered by chat type.

        Returns:
            QuerySet[ConversationThread]: Filtered queryset of conversation threads.
        """
        chat_type: str | None = self.request.GET.get("chat_type")
        if chat_type == "api":
            return ConversationThread.objects.filter(
                created_by=self.request.user, chat_type="api"
            )
        elif chat_type == "web":
            return ConversationThread.objects.filter(
                created_by=self.request.user, chat_type="web"
            )
        elif chat_type == "noa":
            return ConversationThread.objects.filter(
                created_by=self.request.user, chat_type="noa"
            )
        else:
            return ConversationThread.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs) -> dict:
        """Add chat_type to the context data.

        Args:
            **kwargs: Additional context keyword arguments.

        Returns:
            dict: Context data with chat_type included.
        """
        context: dict = super().get_context_data(**kwargs)
        context["chat_type"] = self.request.GET.get("chat_type", "all")
        return context


class ConversationThreadDetailView(
    ProjectNameMixin,
    ConversationThreadViewPermissionTestMixin,
    UserPassesTestMixin,
    LoginRequiredMixin,
    DetailView,
):
    """Detail view for a single ConversationThread.

    Displays the details of a conversation thread and provides a form for adding conversation items.
    """

    model = ConversationThread
    context_object_name = "latest_conversation"
    template_name = "chats/chats_detail.html"
    form_class = ConversationItemForm

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Handle GET requests for the conversation thread detail view.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response for the detail view.
        """
        try:
            return super().get(request, *args, **kwargs)
        except ConversationThread.DoesNotExist:
            return self.response_class(
                request=self.request,
                template="home/logged_in_sections/start_first_chat.html",
                context={},
                using=self.template_engine,
            )

    def get_context_data(self, **kwargs) -> dict:
        """Add a form to the context data for the detail view.

        Args:
            **kwargs: Additional context keyword arguments.

        Returns:
            dict: Context data with form included.
        """
        context_data: dict = super().get_context_data(**kwargs)
        context_data["form"] = self.form_class()
        return context_data

    def get_object(self, queryset: QuerySet | None = None) -> ConversationThread:
        """Return the ConversationThread object for the detail view.

        Args:
            queryset (QuerySet | None): Optional queryset to use.

        Returns:
            ConversationThread: The conversation thread object.

        Raises:
            AttributeError: If neither pk nor slug is provided in the URLconf.
            queryset.model.DoesNotExist: If the object does not exist.
        """
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            try:
                queryset = queryset.filter(pk=pk)
            except Exception:
                queryset = queryset.filter(pk=queryset.first().pk)
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            obj: ConversationThread = queryset.get()
        except queryset.model.DoesNotExist as ex:
            raise ex
        return obj


""" SECTION 3 """


class ConversationThreadCreateView(LoginRequiredMixin, CreateView):
    """Create view for ConversationThread objects.

    Allows authenticated users to create new conversation threads and displays the associated form.
    """

    model = ConversationThread
    form_class = ConversationThreadForm
    context_object_name = "conversation_thread"
    template_name = "chats/chats_detail.html"

    def get_context_data(self, **kwargs) -> dict:
        """Add the new chat form to the context data.

        Args:
            **kwargs: Additional context keyword arguments.

        Returns:
            dict: Context data with new_chat_form included.
        """
        kwargs = super().get_context_data(**kwargs)
        kwargs["new_chat_form"] = kwargs["form"]
        return kwargs

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Handle POST requests for creating a new conversation thread.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response after creating the thread.
        """
        response = super().post(request, *args, **kwargs)
        response.headers["HX-Trigger"] = "newChatList"
        return response

    def form_valid(self, form: ConversationThreadForm) -> HttpResponse:
        """Handle a valid form submission for creating a conversation thread.

        Args:
            form (ConversationThreadForm): The validated form instance.

        Returns:
            HttpResponse: The HTTP response with the new conversation thread.
        """
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        self.object = form.save()
        latest_conversation = form.instance
        return self.render_to_response(
            self.get_context_data(
                form=ConversationItemForm(), latest_conversation=latest_conversation
            )
        )


class ConversationThreadDeleteView(
    ConversationThreadViewPermissionTestMixin,
    UserPassesTestMixin,
    LoginRequiredMixin,
    DeleteView,
):
    """Delete view for ConversationThread objects.

    Allows authenticated users to delete conversation threads and returns a no-content response.
    """

    model = ConversationThread
    context_object_name = "conversation_thread"
    template_name = "chats/chats_delete.html"
    success_url = reverse_lazy("home")

    class HttpResponseNoContent(HttpResponse):
        """HTTP response with 204 No Content status."""

        status_code = HTTPStatus.NO_CONTENT

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Handle POST requests for deleting a conversation thread.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response after deleting the thread.
        """

        response: HttpResponse = super().post(request, *args, **kwargs)
        response.headers["HX-Trigger"] = "newChatList, deleteChat"
        return response

    def form_valid(self, form) -> HttpResponse:
        """Handle a valid form submission for deleting a conversation thread.

        Args:
            form: The validated form instance.

        Returns:
            HttpResponse: The HTTP response after deletion.
        """
        self.object.delete()
        object_list = ConversationThread.objects.filter(
            created_by=self.request.user, chat_type="api"
        )
        return self.render_to_response_post(
            {
                "conversation_threads": object_list,
            }
        )

    def render_to_response_post(self, context: dict, **response_kwargs) -> HttpResponse:
        """Return a 204 No Content response after deletion.

        Args:
            context (dict): Context data for the response.
            **response_kwargs: Additional response keyword arguments.

        Returns:
            HttpResponse: The HTTP 204 No Content response.
        """
        response_kwargs.setdefault("content_type", self.content_type)
        return self.HttpResponseNoContent()


@login_required
@csrf_protect
def send_prompt(request, thread_id=None) -> HttpResponse:
    """Handle sending a prompt to a conversation thread.

    Processes POST requests to add a prompt to a conversation thread and returns the updated conversation.
    For GET requests, displays an empty prompt form.

    Args:
        request (HttpRequest): The HTTP request object.
        thread_id (int | None): The ID of the conversation thread, if any.

    Returns:
        HttpResponse: The HTTP response with the updated conversation or form.
    """
    if request.method == "POST":
        # Get or create thread
        if thread_id:
            conversation_thread: ConversationThread = get_object_or_404(
                ConversationThread, id=thread_id, created_by=request.user
            )
        else:
            conversation_thread: ConversationThread = ConversationThread.objects.create(
                name="New Conversation", created_by=request.user, chat_type="web"
            )
        aimodel = conversation_thread.aimodel

        post_data: dict = request.POST.copy()
        post_data["conversation_thread"] = conversation_thread.id

        # Bind form with POST data (now includes conversation_thread)
        form_from_prompt: ConversationItemForm = ConversationItemForm(post_data)
        form_from_prompt.instance.conversation_thread = conversation_thread
        form_from_prompt.instance.created_by = request.user
        form_from_prompt.instance.modified_by = request.user

        # Set ORDER if not provided
        if not form_from_prompt.instance.ORDER:
            last_item: ConversationItem | None = (
                ConversationItem.objects.filter(conversation_thread=conversation_thread)
                .order_by("-ORDER")
                .first()
            )
            form_from_prompt.instance.ORDER = (last_item.ORDER + 1) if last_item else 1

        if not form_from_prompt.is_valid():
            # Return form with errors
            return render(
                request,
                "home/logged_in_sections/chat_prompt.html",
                {"form": form_from_prompt, "thread_id": conversation_thread.id},
                status=400,
            )

        prompt: str = form_from_prompt.cleaned_data["prompt"]
        aimodel_response = aimodel.get_aimodel_response(prompt)

        conversation_item: ConversationItem = form_from_prompt.save(commit=False)
        conversation_item.response = aimodel_response.choices[0].message.content
        conversation_item.tokens = len(prompt.split())
        conversation_item.save()

        # Render updated prompt/response and new form
        form_for_response: ConversationItemForm = ConversationItemForm(
            initial={
                "conversation_thread": conversation_thread.id,
                "ORDER": form_from_prompt.instance.ORDER + 1,
            }
        )
        return render(
            request,
            "home/logged_in_sections/send_prompt.html",
            {
                "conversation_item": conversation_item,
                "form": form_for_response,
                "latest_conversation": conversation_thread,
            },
        )
    else:
        # GET: show empty form
        form_from_prompt: ConversationItemForm = ConversationItemForm()
        return render(
            request,
            "home/logged_in_sections/chat_prompt.html",
            {"form": form_from_prompt, "thread_id": thread_id},
        )
