from hmac import new

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import resolve, reverse

from project_apps.aimodels.tests.tests_models import create_ai_model
from project_apps.chats.models import ConversationItem, ConversationThread
from project_apps.chats.tests.tests_models import (
    create_conversation_items,
    create_conversation_thread,
)
from standard.tests.utils import generate_request

from .views import HomePageView


class HomepageTest(TestCase):
    username = "newuser"
    email = "newuser@address.com"
    password = "testpass123"

    def setUp(self):
        self.url = reverse("home")
        self.response = self.client.get(self.url, follow=True)
        self.new_user = get_user_model().objects.create_user(
            self.username, self.email, password=self.password
        )
        self.ai_model = create_ai_model(
            self.new_user,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_url_resolves_homepageview(self):
        view = resolve("/")
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)

    def test_homepage_with_no_user_loged_in(self):
        self.assertTemplateUsed(self.response, "account/login.html")
        self.assertContains(self.response, "Login")
        self.assertContains(self.response, "Email address")
        self.assertContains(self.response, "Password")

    def test_homepage_with_user_logged_in(self):
        conversationthread = create_conversation_thread(
            self.new_user, "Test WEB Thread 1", "Test Summary 1", "web", self.ai_model
        )
        create_conversation_items(self.new_user, conversationthread)
        conversationthread = create_conversation_thread(
            self.new_user, "Test WEB Thread 2", "Test Summary 2", "web", self.ai_model
        )
        create_conversation_items(self.new_user, conversationthread)
        conversationthread = create_conversation_thread(
            self.new_user, "Test API Thread 1", "Test Summary 1", "api", self.ai_model
        )
        conversationthread = create_conversation_thread(
            self.new_user, "Test API Thread 2", "Test Summary 2", "api", self.ai_model
        )

        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(self.response, "home/homepagecontent.html")
        self.assertContains(self.response, "AIUI")
        self.assertContains(self.response, "newuser@address.com")
        self.assertContains(self.response, "No conversations yet.")
        self.assertContains(self.response, "AIUI Chat")
        self.assertContains(self.response, "NOA Conversations")
        self.assertContains(self.response, "API Conversations")
        self.assertContains(self.response, "Knowledge")
        self.assertContains(self.response, "Conversation Threads")
        self.assertContains(self.response, "Test WEB Thread 1")
        self.assertContains(self.response, "Test WEB Thread 2")

    def test_homepage_with_user_logged_in_no_conversations(self):
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(self.response, "home/homepagecontent.html")
        self.assertContains(self.response, "AIUI")
        self.assertContains(self.response, "newuser@address.com")
        self.assertContains(self.response, "No conversations yet.")
        self.assertContains(self.response, "AIUI Chat")
        self.assertContains(self.response, "NOA Conversations")
        self.assertContains(self.response, "API Conversations")
        self.assertContains(self.response, "Knowledge")
        self.assertContains(self.response, "Conversation Threads")
        self.assertNotContains(self.response, "Test WEB Thread 1")
        self.assertNotContains(self.response, "Test WEB Thread 2")


@override_settings(SECURE_SSL_REDIRECT=False)
class SendPromptViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.url = reverse("send_prompt")  # Adjust if you use a different name
        self.client.login(username="testuser", password="testpass")

    def test_get_returns_form(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/logged_in_sections/chat_prompt.html")
        self.assertIn("form", response.context)
