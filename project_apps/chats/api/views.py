"""api/views.py

This module provides an API endpoint that mimics the NOA API for BrilliantLabs Frame AR glasses.
It handles multimodal requests (text, audio, images) and returns structured responses using AI models.
"""

import json
import logging
import tempfile

import whisper
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from project_apps.aimodels.models import AIModel
from project_apps.chats.models import ConversationItem, ConversationThread

from .serializers import MultimodalRequestSerializer, MultimodalResponseSerializer

logger = logging.getLogger(__name__)


class NOAMultiModalEndpoint(APIView):
    """
    Provides an API endpoint for handling multimodal requests from BrilliantLabs Frame AR glasses.
    Accepts text, audio, and image inputs, processes them, and returns structured AI-generated responses.

    This endpoint mimics the NOA API, supporting anonymous access and integrating with AI models for response generation.
    """

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]  # No auth required per specs
    aimodel_name = "openai/gpt-oss-20b:free"

    def post(self, request, *args, **kwargs) -> Response:
        """
        Handles POST requests for the NOA multimodal endpoint.

        Processes incoming multimodal data, including text, audio, and images, and returns a structured AI response.

        Args:
            request: The HTTP request object containing multimodal data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A DRF Response object containing the AI-generated structured response or error details.
        """
        try:
            return self._process_multimodal_request(request)
        except json.JSONDecodeError:
            return Response({"detail": "Invalid JSON in mm parameter"}, status=400)
        except Exception as e:
            logger.exception("Error processing NOA request")
            return Response(
                {"detail": f"Exception: {str(e)}"},
                status=e.status_code if hasattr(e, "status_code") else 500,
            )

    def _process_multimodal_request(self, request) -> Response:
        """
        Processes the multimodal request and orchestrates extraction, validation, AI response,
        and formatting.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A DRF Response object with the validated AI response or error details.
        """
        multimodal_data: dict = self._extract_multimodal_data(request.POST)
        validated_data: dict | None = self._validate_multimodal_data(multimodal_data)
        if not validated_data:
            return Response({"detail": "Invalid multimodal data"}, status=400)

        prompt: str = validated_data.get("prompt", "No Prompt Provided")
        # other possible multimodal data items for processing
        # messages = validated_data.get("messages", [])
        # address = validated_data.get("address", "")
        # local_time = validated_data.get("local_time", "")

        audio_text: str = self._transcribe_user_prompt_from_audio(
            request.FILES.get("audio")
        )
        image = self._process_image_file(request.FILES.get("image"))

        full_user_prompt: str = self._build_full_prompt(prompt, audio_text)
        aimodel = self._get_aimodel()
        aimodel_response = self._generate_response(full_user_prompt, aimodel)
        response_text: str = (
            aimodel_response.choices[0].message.content.strip()
            if aimodel_response
            else "No response generated"
        )

        self._save_conversation(aimodel, full_user_prompt, response_text)

        response_data: dict = self._prepare_noa_response_data(
            full_user_prompt, response_text
        )

        validated_response_data: dict | None = self._validate_response_data(
            response_data
        )
        return (
            Response(validated_response_data)
            if validated_response_data
            else Response({"detail": "Server error in response formatting"}, status=500)
        )

    def _extract_multimodal_data(self, mm_data: dict) -> dict:
        """
        Extracts and transforms multimodal data from the request to match serializer expectations.

        Args:
            mm_data: Dictionary containing the raw multimodal data from the request.

        Returns:
            dict: A dictionary with parsed and mapped multimodal data fields.
        """
        multimodal_data: dict = {}

        # Parse messages if present
        if "messages" in mm_data:
            try:
                import json

                multimodal_data["messages"] = json.loads(mm_data["messages"])
            except json.JSONDecodeError:
                return Response(
                    {"detail": "Invalid JSON in messages field"}, status=400
                )

        # Map other fields
        multimodal_data["address"] = mm_data.get("location", "")
        multimodal_data["local_time"] = mm_data.get("time", "")
        multimodal_data["prompt"] = mm_data.get("prompt", "")

        # Copy any other fields that might be present - These are just examples.
        # Maybe with your own version of the NOA app.
        # for key in ["gps", "vision", "assistant", "assistant_model"]:
        #     if key in mm_data:
        #         multimodal_data[key] = mm_data[key]
        return multimodal_data

    def _transcribe_user_prompt_from_audio(self, audio_file) -> str:
        """
        Transcribes audio input to text using the Whisper model.

        Args:
            audio_file: The uploaded audio file.

        Returns:
            str: The transcribed text from the audio, or an empty string if no audio is provided.
        """
        audio_text: str = ""
        if audio_file:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio:
                for chunk in audio_file.chunks():
                    temp_audio.write(chunk)
                temp_audio.flush()
                model = whisper.load_model("small")
                transcription_result: dict = model.transcribe(temp_audio.name)
                audio_text = transcription_result["text"].strip()
                logger.info(f"Received audio file: {audio_file.name}")

        return audio_text

    def _process_image_file(self, image_file) -> object | None:
        """
        Processes the uploaded image file for vision features.

        Args:
            image_file: The uploaded image file.

        Returns:
            The image file if provided, otherwise None.
        """
        if image_file:
            # In a real implementation, you might process the image for vision features
            logger.info(f"Received image file: {image_file.name}")
            return image_file
        else:
            logger.info("No image file received")
            return None

    def _build_full_prompt(self, prompt: str, audio_text: str) -> str:
        """
        Builds the full user prompt by combining text and transcribed audio.

        Args:
            prompt: The text prompt from the user.
            audio_text: The transcribed audio text.

        Returns:
            str: The combined prompt string.
        """
        # This could also include a system prompt or other context.
        return f"{prompt} {audio_text}".strip()

    def _generate_response(self, full_user_prompt: str, aimodel: AIModel) -> object:
        """
        Generates a response from the AI model based on the full user prompt.

        Args:
            full_user_prompt: The complete prompt string for the AI model.
            aimodel: The AIModel instance to use for generating the response.

        Returns:
            object or None: The AI model's response object.
        """
        # In a real implementation, you might call an AI model here
        # Call the AI model to get a response
        # Model name is a placeholder.
        # This should grab models as required by prompt.
        return (
            aimodel.get_aimodel_response(full_user_prompt) if full_user_prompt else None
        )

    def _save_conversation(
        self, aimodel: AIModel, user_prompt: str, response_text: str
    ) -> ConversationItem | None:
        """
        Saves the conversation thread and item for the current interaction.

        Args:
            aimodel: The AIModel instance used.
            user_prompt: The user's full prompt.
            response_text: The AI-generated response text.

        Returns:
            ConversationItem or None: The saved conversation item, or None if not saved.
        """
        conversation_thread: ConversationThread | None = self._get_conversation_thread(
            aimodel
        )
        return self._save_conversation_item(
            conversation_thread, user_prompt, response_text
        )

    def _get_conversation_thread(self, aimodel: AIModel) -> ConversationThread | None:
        """
        Retrieves or creates a conversation thread for the current session.

        Placeholder for actual thread creation logic.

        Args:
            aimodel: The AIModel instance used.

        Returns:
            ConversationThread: Should return the conversation thread
        """
        # Create thread if this is a new conversation
        # For now, create a new thread for each request as placeholder
        # conversation_thread = ConversationThread.objects.create(
        #     id=uuid.uuid4(),
        #     user=None,  # Anonymous for NOA requests
        #     name=f"NOA Chat {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        #     summary='A summary based on the user prompt and AI response'
        #     type="noa",
        #     is_active=True,
        #     aimodel=aimodel
        # )
        pass

    def _save_conversation_item(
        self,
        conversation_thread: ConversationThread | None,
        full_prompt: str,
        response_text: str,
    ) -> ConversationItem | None:
        """
        Saves a conversation item to the database.

        Placeholder for actual item saving logic.

        Args:
            conversation_thread: The conversation thread instance.
            full_prompt: The full user prompt.
            response_text: The AI-generated response text.

        Returns:
            ConversationItem: Should return the conversation item
        """
        # Save the conversation item
        # item = ConversationItem.objects.create(
        #     id=uuid.uuid4(),
        #     conversation_thread=conversation_thread,
        #     prompt=full_prompt,
        #     response=response_text,
        #     tokens=len(full_prompt.split())
        #     + len(response_text.split()),  # Simple token counting
        #     is_full_saved=True,
        # )
        pass

    def _prepare_noa_response_data(
        self, full_user_prompt: str, response_text: str
    ) -> dict:
        """
        Prepares the response data structure for the NOA API.

        Args:
            full_user_prompt: The full user prompt string.
            response_text: The AI-generated response text.

        Returns:
            dict: The structured response data.
        """
        # A more complete response
        # response_data = {
        #     "user_prompt": user_prompt,
        #     "response": response_text,
        #     "image": None,  # Changed to null/None to match example
        #     "token_usage_by_model": {
        #         "gpt-4o": {
        #             "input_tokens": 40,
        #             "output_tokens": 60,
        #         }
        #     },
        #     "capabilities_used": ["assistant_knowledge"],
        #     "total_tokens": 100,
        #     "input_tokens": 40,
        #     "output_tokens": 60,
        #     "timings": "Total: 0.5s, Assistant: 0.5s",  # Updated to match example format
        #     "debug_tools": {
        #         "topic_changed": False
        #     },  # Empty string instead of "None"
        # }
        return {
            "user_prompt": full_user_prompt,
            "message": response_text,
            "debug": {"topic_changed": False},
        }

    def _get_aimodel(self) -> AIModel:
        """
        Retrieves the AIModel instance by name.

        Returns:
            AIModel: The AIModel instance.
        """
        return AIModel.objects.get(name=self._get_aimodel_name())

    def _get_aimodel_name(self) -> str:
        """
        Retrieves the AIModel name.

        This function can be a hook for more complicated decision-making logic about
        AI models to use in the future.

        Returns:
            str: The AIModel name.
        """
        return self.aimodel_name

    def _validate_multimodal_data(self, data: dict) -> dict | None:
        """
        Validates the multimodal request data using the serializer.

        Args:
            data: The multimodal data dictionary.

        Returns:
            dict or None: The validated data if valid, otherwise None.
        """
        serializer = MultimodalRequestSerializer(data=data)
        return serializer.validated_data if serializer.is_valid() else None

    def _validate_response_data(self, data: dict) -> dict | None:
        """
        Validates the response data structure using the serializer.

        Args:
            data: The response data dictionary.

        Returns:
            dict or None: The validated response data if valid, otherwise None.
        """
        response_serializer = MultimodalResponseSerializer(data=data)
        return (
            response_serializer.validated_data
            if response_serializer.is_valid()
            else None
        )
