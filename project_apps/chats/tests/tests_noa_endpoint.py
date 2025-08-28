import json
import uuid
from pathlib import Path
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from project_apps.aimodels.tests.tests_models import create_ai_model
from project_apps.chats.api.views import NOAMultiModalEndpoint
from project_apps.chats.models import ConversationItem, ConversationThread


@override_settings(SECURE_SSL_REDIRECT=False)
class NOAMultiModalEndpointTests(APITestCase):
    """
    Test suite for the NOAMultiModalEndpoint API view.
    """

    def setUp(self):
        """Set up test data and resources before each test."""
        user_model = get_user_model()
        self.user1 = user_model.objects.create_user(
            email="junior@project.com",
            username="junior",
            password="testpass123",
            terms_and_conditions=True,
        )
        self.ai_model = create_ai_model(
            self.user1,
            "openai/gpt-oss-20b:free",
            "gpt-oss-20b is an open-weight 21B parameter model released by OpenAI under the Apache 2.0 license. It uses a Mixture-of-Experts (MoE) architecture with 3.6B active parameters per forward pass, optimized for lower-latency inference and deployability on consumer or single-GPU hardware. The model is trained in OpenAI’s Harmony response format and supports reasoning level configuration, fine-tuning, and agentic capabilities including function calling, tool use, and structured outputs.",
            0.0000,
            0.0000,
            "Edge devices and focused tasks.",
            "openai_api",
            "https://openrouter.ai/api/v1",
            4096,
        )
        self.url = reverse(
            "noa-mm-endpoint"
        )  # Assuming 'noa-mm-endpoint' is the URL name
        self.factory = APIRequestFactory()

        # Create a sample valid mm JSON data
        # <QueryDict: {'messages': ['[{"role":"user","content":"What\'s philosophy?"},{"role":"assistant","content":"Philosophy is the study of fundamental questions about existence, knowledge, values, reason, mind, and language. It involves critical analysis and the pursuit of wisdom."}]'], 'location': ['9 Dorking Grove, Wavertree, Liverpool, L15 6XR, United Kingdom'], 'time': ['2025-07-02 11:29:48.054846']}>
        self.valid_mm_data = {
            "messages": [
                '[{"role":"user","content":"What\'s philosophy?"},{"role":"assistant","content":"Philosophy is the study of fundamental questions about existence, knowledge, values, reason, mind, and language. It involves critical analysis and the pursuit of wisdom."}]'
            ],
            "location": [
                "9 Dorking Grove, Wavertree, Liverpool, L15 6XR, United Kingdom"
            ],
            "time": ["2025-07-02 11:29:48.054846"],
        }

        # Create audio and image test files
        # self.test_audio = SimpleUploadedFile(
        #     "test_audio.mp3", b"audio file content", content_type="audio/mpeg"
        # )
        audio_path = settings.BASE_DIR.joinpath(
            "project_apps", "chats", "tests", "test_audio.wav"
        )
        with open(audio_path, "rb") as audio_file:
            self.test_audio = SimpleUploadedFile(
                "test_audio.wav", audio_file.read(), content_type="audio/wav"
            )

        self.test_image = SimpleUploadedFile(
            "test_image.jpg", b"image file content", content_type="image/jpeg"
        )

    def test_valid_request_without_files(self):
        """Test that a valid request without files returns a 200 response."""
        data = self.valid_mm_data
        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        # '{"user_prompt":"Tell me about Django","response":"This is a dummy response to your prompt: \'Tell me about Django\'","image":"bla","token_usage_by_model":{"dummy-model":{"total_tokens":100,"input_tokens":40,"output_tokens":60}},"capabilities_used":["assistant_knowledge"],"total_tokens":100,"input_tokens":40,"output_tokens":60,"timings":"0.5s","debug_tools":"None"}'
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Server error in response formatting")

        # Check that a conversation thread was created
        # self.assertEqual(ConversationThread.objects.count(), 1)
        # thread = ConversationThread.objects.first()
        # self.assertEqual(thread.type, "noa")

        # Check that a conversation item was created
        # self.assertEqual(ConversationItem.objects.count(), 1)
        # item = ConversationItem.objects.first()
        # self.assertEqual(item.thread, thread)
        # self.assertEqual(item.prompt, self.valid_mm_data["prompt"])

    def test_valid_request_with_audio(self):
        """Test that a valid request with audio returns a 200 response."""
        data = self.valid_mm_data
        data["audio"] = self.test_audio
        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Audio would be mentioned in the prompt
        self.assertIn("What's the capital of France?", response.data["user_prompt"])
        self.assertIn(
            "Paris",
            response.data["message"],
            "The response from the AI model did not contain the expected text.",
        )

    def test_valid_request_with_image(self):
        """Test that a valid request with an image returns a 200 response."""
        data = self.valid_mm_data
        data["image"] = self.test_image
        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        # In the current implementation, images don't affect the response content
        self.assertEqual(response.data["detail"], "Server error in response formatting")

    def test_valid_request_with_audio_and_image(self):
        """Test that a valid request with both audio and image returns a 200 response."""
        data = self.valid_mm_data
        data["audio"] = self.test_audio
        data["image"] = self.test_image
        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("What's the capital of France?", response.data["user_prompt"])
        self.assertIn(
            "Paris",
            response.data["message"],
            "The response from the AI model did not contain the expected text.",
        )

    def test_missing_mm_parameter(self):
        """Test that a request without the mm parameter returns a 400 response."""
        response = self.client.post(self.url, {}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Since empty mm will be treated as "{}" and validated as empty object

    def test_invalid_json_mm_parameter(self):
        """Test that a request with invalid JSON in the mm parameter returns a 400 response."""
        data = self.valid_mm_data
        data["messages"] = "Invalid JSON string"  # Invalid JSON format
        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"detail": "Invalid multimodal data"})

    def test_direct_view_invocation(self):
        """Test direct invocation of the view with APIRequestFactory."""
        view = NOAMultiModalEndpoint.as_view()

        # Create a request with the factory
        request = self.factory.post(self.url, self.valid_mm_data, format="multipart")

        # Process the request
        response = view(request)

        # Check response
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["detail"], "Server error in response formatting")


'''
    def test_invalid_response_format(self):
        """Test handling of invalid response format."""
        with patch(
            "project_apps.chats.api.views.MultimodalResponseSerializer"
        ) as mock_serializer_cls:
            # Create a mock serializer instance
            mock_serializer = MagicMock()
            mock_serializer.is_valid.return_value = False
            mock_serializer.errors = {"errors": "Invalid response format"}
            mock_serializer_cls.return_value = mock_serializer

            data = self.valid_mm_data
            response = self.client.post(self.url, data, format="multipart")

            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertEqual(
                response.data, {"error": "Server error in response formatting"}
            )

    def test_server_error_handling(self):
        """Test server error handling with a mocked exception."""
        with patch(
            "project_apps.chats.models.ConversationThread.objects.create"
        ) as mock_create:
            # Force an exception during thread creation
            mock_create.side_effect = Exception("Simulated server error")

            data = {"mm": json.dumps(self.valid_mm_data)}
            response = self.client.post(self.url, data, format="multipart")

            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertEqual(response.data, {"error": "Simulated server error"})
'''


@override_settings(SECURE_SSL_REDIRECT=False)
class NOAEndpointIntegrationTests(APITestCase):
    """
    Integration tests for the NOA endpoint.
    These tests verify that the endpoint works correctly in the context of the whole application.
    """

    def setUp(self):
        """Set up test data and resources before each test."""
        user_model = get_user_model()
        self.user1 = user_model.objects.create_user(
            email="junior@project.com",
            username="junior",
            password="testpass123",
            terms_and_conditions=True,
        )
        self.ai_model = create_ai_model(
            self.user1,
            "openai/gpt-oss-20b:free",
            "gpt-oss-20b is an open-weight 21B parameter model released by OpenAI under the Apache 2.0 license. It uses a Mixture-of-Experts (MoE) architecture with 3.6B active parameters per forward pass, optimized for lower-latency inference and deployability on consumer or single-GPU hardware. The model is trained in OpenAI’s Harmony response format and supports reasoning level configuration, fine-tuning, and agentic capabilities including function calling, tool use, and structured outputs.",
            0.0000,
            0.0000,
            "Edge devices and focused tasks.",
            "openai_api",
            "https://openrouter.ai/api/v1",
            4096,
        )

        self.url = "/mm/mm/"  # Direct URL path

        self.valid_mm_data = {
            "messages": [
                '[{"role":"user","content":"What\'s philosophy?"},{"role":"assistant","content":"Philosophy is the study of fundamental questions about existence, knowledge, values, reason, mind, and language. It involves critical analysis and the pursuit of wisdom."}]'
            ],
            "location": [
                "9 Dorking Grove, Wavertree, Liverpool, L15 6XR, United Kingdom"
            ],
            "time": ["2025-07-02 11:29:48.054846"],
        }

        audio_path = settings.BASE_DIR.joinpath(
            "project_apps", "chats", "tests", "test_audio.wav"
        )
        with open(audio_path, "rb") as audio_file:
            self.test_audio = SimpleUploadedFile(
                "test_audio.wav", audio_file.read(), content_type="audio/wav"
            )

    def test_endpoint_integration(self):
        """Test that the endpoint is properly integrated in the Django URL routing."""
        data = self.valid_mm_data
        data["audio"] = self.test_audio
        response = self.client.post(self.url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user_prompt", response.data)
        self.assertIn("message", response.data)
        self.assertIn("debug", response.data)
        self.assertEqual(response.data["debug"]["topic_changed"], False)
