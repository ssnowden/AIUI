"""This module unit tests the views for the chats app.

It has the test cases:
    ListViewTest: Showing a list of ConversationThread model.
    DetailViewTest: Showing the details of an instance of ConversationThread model.
    CreateViewTest: Enabling the creation of an instance of ConversationThread model.
    DeleteViewTest Enabling the delete of an instance of ConversationThread model.

"""

from http import HTTPStatus

from django.test import TestCase, tag

from standard.tests import utils as test_utils
from standard.tests.utils import UserSetupMixin
from standard.tests.views import BaseViewEditTestMixin, BaseViewTestMixin

from project_apps.chats.models import ConversationThread

from project_apps.chats.forms import ConversationThreadForm

from project_apps.chats.views import (
    ConversationThreadCreateView,
    ConversationThreadDeleteView,
    ConversationThreadDetailView,
    ConversationThreadListView,
)

from project_apps.aimodels.tests.tests_models import create_ai_model
from project_apps.chats.tests.tests_models import (
    create_conversation_item,
    create_conversation_items,
    create_conversation_thread,
)


@tag("view")
class TestListView(UserSetupMixin, BaseViewTestMixin, TestCase):
    """
    This class performs basic tests for the List View focused on ConversationThread

    Attributes:

    methods:
        BaseViewTestMixin
            setUp
            test_view_initial_setup
            test_view_with_anonymous_and_existing_users
        test_procedures_conversationthread_view_for_object_data
        test_procedures_conversationthread_view_for_object_data_empty
    """

    view = ConversationThreadListView
    view_object_name = "conversation_threads"
    model = ConversationThread
    template_name = "chats/list/chats_list.html"
    view_url = "chats/"
    id_for_object_view = None

    def setUp(self):
        super().setUp()
        self.ai_model = create_ai_model(
            self.user1,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )

    def test_view_rendering(self):
        conversationthread = create_conversation_thread(
            self.user1, "Test WEB Thread 1", "Test Summary 1", "web", self.ai_model
        )
        conversationthread = create_conversation_thread(
            self.user1, "Test WEB Thread 2", "Test Summary 2", "web", self.ai_model
        )
        conversationthread = create_conversation_thread(
            self.user1, "Test API Thread 1", "Test Summary 1", "api", self.ai_model
        )
        conversationthread = create_conversation_thread(
            self.user2, "Test WEB Thread 3", "Test Summary 3", "web", self.ai_model
        )

        request = test_utils.generate_request("GET", f"{self.view_url}", self.user1)
        conversationthread_list_view = test_utils.setup_view_request(self.view, request)

        conversationthread_list_view.object_list = (
            conversationthread_list_view.get_queryset()
        )

        context = conversationthread_list_view.get_context_data()
        response = conversationthread_list_view.render_to_response(context)
        response.render()
        self.assertContains(response, "Test WEB Thread 1")
        self.assertNotContains(response, "Test Summary 1")
        self.assertContains(response, "Test API Thread 1")
        self.assertNotContains(response, "Test WEB Thread 3")
        self.assertTemplateUsed(self.template_name)

        request = test_utils.generate_request(
            "GET", self.view_url, self.user1, query_string="chat_type=web"
        )
        conversationthread_list_view = test_utils.setup_view_request(self.view, request)

        conversationthread_list_view.object_list = (
            conversationthread_list_view.get_queryset()
        )

        context = conversationthread_list_view.get_context_data()
        response = conversationthread_list_view.render_to_response(context)
        response.render()
        self.assertContains(response, "Test WEB Thread 1")
        self.assertNotContains(response, "Test Summary 1")
        self.assertNotContains(response, "Test API Thread 1")
        self.assertNotContains(response, "Test WEB Thread 3")
        self.assertTemplateUsed(self.template_name)

        request = test_utils.generate_request(
            "GET", self.view_url, self.user1, query_string="chat_type=api"
        )
        conversationthread_list_view = test_utils.setup_view_request(self.view, request)

        conversationthread_list_view.object_list = (
            conversationthread_list_view.get_queryset()
        )

        context = conversationthread_list_view.get_context_data()
        response = conversationthread_list_view.render_to_response(context)
        response.render()
        self.assertNotContains(response, "Test WEB Thread 1")
        self.assertNotContains(response, "Test Summary 1")
        self.assertContains(response, "Test API Thread 1")
        self.assertNotContains(response, "Test WEB Thread 3")
        self.assertTemplateUsed(self.template_name)

    def test_view_rendering_empty_list(self):
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        conversationthread_list_view = test_utils.setup_view_request(self.view, request)

        conversationthread_list_view.object_list = (
            conversationthread_list_view.get_queryset()
        )

        context = conversationthread_list_view.get_context_data()
        response = conversationthread_list_view.render_to_response(context)
        response.render()
        self.assertContains(response, "No chats yet.")
        self.assertTemplateUsed(self.template_name)


@tag("view")
class DetailViewTest(UserSetupMixin, BaseViewTestMixin, TestCase):
    """
    This class performs basic tests for the Detail View focused on ConversationThread

    Attributes:

    methods:
        BaseViewTestMixin
            setUp
            test_view_initial_setup
            test_view_with_anonymous_and_existing_users
        setUp
        test_conversationthread_detail_view_for_object_data
        test_conversationthread_detail_view_for_object_data_empty
        test_view_rendering
    """

    view = ConversationThreadDetailView
    view_object_name = "latest_conversation"
    model = ConversationThread
    template_name = "chats/chats_detail.html"
    view_url = "chats/"

    def setUp(self):
        super().setUp()
        self.ai_model = create_ai_model(
            self.user2,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )
        self.instance = create_conversation_thread(
            self.user1, "Test WEB Thread 1", "Test Summary 1", "web", self.ai_model
        )
        create_conversation_item(
            self.user1, self.instance, "Prompt 1", "Response 1", 1, 0
        )
        create_conversation_item(
            self.user1, self.instance, "Prompt 2", "Response 2", 1, 0
        )
        create_conversation_item(
            self.user1, self.instance, "Prompt 3", "Response 3", 1, 0
        )

        self.view_url = f"{self.view_url}{self.instance.id}/"
        self.id_for_object_view = self.instance.id

    def test_view_rendering(self):
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        conversation_thread_detail_view = test_utils.setup_view_request(
            self.view, request, self.instance.id
        )

        data = conversation_thread_detail_view.get_queryset()
        self.assertTrue(data.exists())

        conversation_thread_detail_view.object = (
            conversation_thread_detail_view.get_object()
        )
        self.assertEqual(
            conversation_thread_detail_view.object.name, "Test WEB Thread 1"
        )
        context = conversation_thread_detail_view.get_context_data()
        response = conversation_thread_detail_view.render_to_response(context)
        response.render()
        self.assertContains(response, "General-purpose coding and writing")
        self.assertContains(response, "Fast completions and visual input understanding")
        self.assertContains(response, "Cost per 1M input tokens:")
        self.assertContains(response, "0.10 USD")
        self.assertContains(response, "Cost per 1M output tokens:")
        self.assertContains(response, "0.50 USD")
        self.assertContains(response, "Prompt 1")
        self.assertContains(response, "Response 1")
        self.assertTemplateUsed(self.template_name)

    def test_view_rendering_no_such_chat(self):
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        conversation_thread_detail_view = test_utils.setup_view_request(
            self.view, request, "test-uuid"
        )

        data = conversation_thread_detail_view.get_queryset()
        self.assertTrue(data.exists())

        conversation_thread_detail_view.object = (
            conversation_thread_detail_view.get_object()
        )
        self.assertEqual(
            conversation_thread_detail_view.object.name, "Test WEB Thread 1"
        )
        context = conversation_thread_detail_view.get_context_data()
        response = conversation_thread_detail_view.render_to_response(context)
        response.render()
        self.assertContains(response, "General-purpose coding and writing")
        self.assertContains(response, "Fast completions and visual input understanding")
        self.assertContains(response, "Cost per 1M input tokens:")
        self.assertContains(response, "0.10 USD")
        self.assertContains(response, "Cost per 1M output tokens:")
        self.assertContains(response, "0.50 USD")
        self.assertContains(response, "Prompt 1")
        self.assertContains(response, "Response 1")
        self.assertTemplateUsed(self.template_name)


@tag("view")
class CreateViewTest(UserSetupMixin, BaseViewEditTestMixin, TestCase):
    """
    This class performs basic tests for the creating lists

    Attributes:

    methods:
        BaseViewTestMixin
            setUp
            test_view_with_anonymous_and_existing_users
        BaseViewEditTestMixin
            test_view_initial_setup
        test_conversationthread_create_view_get
        test_conversationthread_create_view_adding_conversationthread_no_conversationitems
        test_conversationthread_create_view_adding_conversationthread_with_conversationitems
        test_conversationthread_create_view_DISALLOW_duplicate_fieldnottobeduplicated
        test_conversationthread_create_view_DISALLOW_duplicate_conversationitem_fieldnottobeduplicated_same_conversationthread
        test_conversationthread_create_view_ALLOW_duplicate_conversationitem_fieldnottobeduplicated_different_conversationthreads
    """

    view = ConversationThreadCreateView
    view_object_name = "conversation_thread"
    model = ConversationThread
    template_name = "chats/chats_detail.html"
    view_url = "chats/create/"
    form = ConversationThreadForm

    def setUp(self):
        super().setUp()
        self.ai_model = create_ai_model(
            self.user2,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )
        self.instance = create_conversation_thread(
            self.user1, "Test API Thread 1", "Test Summary 1", "api", self.ai_model
        )
        # create_conversationitems(self.user1, self.instance)
        self.id_for_object_view = None

    def test_conversationthread_create_view_adding_conversation_thread_no_conversationitems(
        self,
    ):
        request = test_utils.generate_request(
            "POST",
            self.view_url,
            self.user1,
            data={
                "name": "Test Conversation",
                "aimodel": self.ai_model.id,
            },
        )
        conversation_thread_create_view = test_utils.setup_view_request(
            self.view, request
        )

        response = conversation_thread_create_view.post(
            conversation_thread_create_view.request,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.headers.get("HX-Trigger"), "newChatList")

        saved_conversation_threads = self.model.objects.all()
        self.assertEqual(
            saved_conversation_threads[1].conversation_items.all().count(), 0
        )

        view_html = response.rendered_content.replace("\n", "")
        html_tests = [
            "40",
            "General-purpose coding and writing",
            f'<form class="pt-3" id="form-container" method="post" hx-post="/chats/send_prompt/{saved_conversation_threads[1].id}" hx-target="#replace-new-reponse-prompt" hx-swap="outerHTML">',
        ]
        for html_test in html_tests:
            self.assertIn(
                html_test,
                view_html,
            )

        test_utils.check_object(
            self,
            saved_conversation_threads[1],
            attribute_tests={
                "name": "Test Conversation",
                "aimodel": str(self.ai_model),
                "created_by": str(self.user1),
                "modified_by": str(self.user1),
            },
        )


@tag("view")
class DeleteViewTest(UserSetupMixin, BaseViewEditTestMixin, TestCase):
    """
    This class performs basic tests for the creating lists

    Attributes:

    methods:
        test_conversationthread_delete_view_get
        test_conversationthread_delete_view_delete_conversationthread
    """

    view = ConversationThreadDeleteView
    view_object_name = "conversation_thread"
    model = ConversationThread
    template_name = "chats/chats_delete.html"
    view_url = "chats/delete/"

    def setUp(self):
        super().setUp()
        self.ai_model = create_ai_model(
            self.user2,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )
        self.instance = create_conversation_thread(
            self.user1, "Test API Thread 1", "Test Summary 1", "api", self.ai_model
        )
        create_conversation_items(self.user1, self.instance)
        self.view_url = f"{self.view_url}{self.instance.id}/"
        self.id_for_object_view = self.instance.id

    def test_conversationthread_delete_view_get(self):
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        conversationthread_delete_view = test_utils.setup_view_request(
            self.view,
            request,
            object_for_test=self.instance.id,
        )

        response = conversationthread_delete_view.get(
            conversationthread_delete_view.request
        )
        self.assertEqual(conversationthread_delete_view.object, self.instance)
        self.assertListEqual(response.template_name, [self.template_name])

        response.resolve_template(self.template_name)

        view_html = response.rendered_content
        self.assertIn("csrfmiddlewaretoken", view_html)
        self.assertIn(
            f'<form class="pt-3" hx-post="/chats/delete/{self.instance.id}/" hx-target="#replace-chats-list" hx-swap="innerHTML" id="chat-delete-form-container">',
            view_html,
        )
        self.assertIn(
            '<div class="modal-dialog">',
            view_html,
        )
        # Expected snippets from the page html
        html_tests = [
            "Test API Thread 1",
            "id-delete-chat",
        ]
        for html_test in html_tests:
            self.assertIn(
                html_test,
                view_html,
            )

    def test_conversationthread_delete_view_delete_conversationthread(self):
        request = test_utils.generate_request(
            "POST",
            self.view_url,
            self.user1,
        )
        conversation_thread_delete_view = test_utils.setup_view_request(
            self.view,
            request,
            object_for_test=self.instance.id,
        )

        response = conversation_thread_delete_view.post(
            request,
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

        saved_conversation_threads = self.model.objects.all()
        self.assertEqual(saved_conversation_threads.count(), 0)
