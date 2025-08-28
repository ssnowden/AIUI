"""This module unit tests the model for the models app.

It has the test cases:
    ModelModelCRUDTest: This ensures that basic CRUD actions can be taken on the Model model.
    ModelModelValidationTest: This ensures that a Model model is validated as required. Also enforces some model best practice (e.g. get_absolute_url).
    ModelItemModelCRUDTest: This ensures that basic CRUD actions can be taken on the ModelItem model.
    ModelItemModelValidationTest: This ensures that a ModelItem model is validated as required. Also enforces some model best practice (e.g. get_absolute_url).

There are also 3 helper functions that are used by these tests but can also be imported into other tests.
    create_model
        Useage:
            from project_apps.models.tests.tests_models import create_model

            create_model(user, field1, field2, field3)

    create_modelitem
        Useage:
            from project_apps.models.tests.tests_models import create_modelitem

            create_modelitem(user, target_model, field1)

    create_modelitems
        Useage:
            from project_apps.lists.tests.tests_models import create_modelitems

            a_model = create_model(user, field1, field2, field3)
            create_modelitems(user, target_model)
"""

from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase, tag

from project_apps.aimodels.models import AIModel
from standard.tests.utils import UserSetupMixin


def create_ai_model(
    user,
    name,
    description,
    token_cost_per_1M_input,
    token_cost_per_1M_output,
    best_use_cases,
    access_mode="openai_api",
    access_endpoint="https://openrouter.ai/api/v1",
    max_tokens=4096,
):
    """
    This is a helper function that creates a Model

    args:
        user: who created the model
        field1: field1 for the modelitem

    returns:
        model: an instance of the a_Model model
    """
    ai_model = AIModel(
        name=name,
        description=description,
        token_cost_per_1M_input=token_cost_per_1M_input,
        token_cost_per_1M_output=token_cost_per_1M_output,
        best_use_cases=best_use_cases,
        access_mode=access_mode,
        access_endpoint=access_endpoint,
        max_tokens=max_tokens,
        created_by=user,
        modified_by=user,
    )
    ai_model.save()
    return ai_model


@tag("model")
class AIModelModelValidationTest(UserSetupMixin, TestCase):
    """
    This class tests validation against constrained attributes of the Model model

    Attributes:

    methods:
        setUp
        test_model_verbose_name_and_verbose_name_plural
        test_model_class_string_set
        test_model_get_absolute_url
        test_model_field_verbose_name
        test_model_choices
    """

    def setUp(self):
        super().setUp()

    def test_model_verbose_name_and_verbose_name_plural(self):
        """
        This function tests that the Model model has verbose name and verbose name plural set.

        args:

        returns:
        """
        self.assertEqual(AIModel._meta.verbose_name_raw, "AI Model")
        self.assertEqual(AIModel._meta.verbose_name_plural, "AI Models")

    def test_model_class_string_set(self):
        """
        This function tests that the Model model has a __string__ set.

        args:

        returns:
        """
        ai_model = create_ai_model(
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
        self.assertEqual(str(ai_model), ai_model.name)

    def test_model_get_absolute_url(self):
        """
        This function tests that the Model model has a get_absolute_url set.

        args:

        returns:
        """
        ai_model = create_ai_model(
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
        self.assertEqual(ai_model.get_absolute_url(), f"/aimodels/{ai_model.id}/")

    def test_model_field_verbose_name(self):
        """
        This function tests that the Model model's fields have verbose name set.

        args:

        returns:
        """
        self.assertEqual(
            AIModel._meta.get_field("name").verbose_name.title(), "Ai Model Name"
        )
        self.assertEqual(
            AIModel._meta.get_field("description").verbose_name.title(),
            "Ai Model Description",
        )
        self.assertEqual(
            AIModel._meta.get_field("token_cost_per_1M_input").verbose_name.title(),
            "Token Cost Per 1M Input",
        )
        self.assertEqual(
            AIModel._meta.get_field("token_cost_per_1M_output").verbose_name.title(),
            "Token Cost Per 1M Output",
        )
        self.assertEqual(
            AIModel._meta.get_field("best_use_cases").verbose_name.title(),
            "Best Use Cases",
        )
        self.assertEqual(
            AIModel._meta.get_field("access_mode").verbose_name.title(),
            "Access Mode",
        )
        self.assertEqual(
            AIModel._meta.get_field("max_tokens").verbose_name.title(),
            "Max Tokens",
        )
        self.assertEqual(
            AIModel._meta.get_field("is_active").verbose_name.title(), "Is Active"
        )

    def test_model_has_required_field(self):
        """
        This function tests that there must be text data for an instance of Model
        ...and if not throws a ValidationError

        args:

        returns:
        """
        ai_model = AIModel(
            name="",
            description="test",
            best_use_cases="best use cases",
            access_mode="openai_api",
            access_endpoint="https://openrouter.ai/api/v1",
            max_tokens=4096,
        )

        with self.assertRaises(ValidationError):
            ai_model.full_clean()

    def test_model_choices(self):
        self.assertTupleEqual(
            AIModel.ACCESS_MODE_CHOICES[0],
            ("openai_api", "OpenAI API"),
            "Missing the ACCESS_MODE_OPENAI_API option",
        )

        self.assertTupleEqual(
            AIModel.ACCESS_MODE_CHOICES[1],
            ("local", "Local Access"),
            "Missing the ACCESS_MODE_LOCAL option",
        )

        self.assertTupleEqual(
            AIModel.ACCESS_MODE_CHOICES[2],
            ("transformer", "Transformer Library"),
            "Missing the ACCESS_MODE_TRANSFORMER option",
        )


@tag("model")
class AIModelModelCRUDTest(UserSetupMixin, TestCase):
    """
    This class performs basic CRUD tests for the Model Model

    Attributes:

    methods:
        setUp
        test_saving_and_retrieving_models
        test_modifying_model
        test_deleting_model
        test_effect_of_deleting_user_on_model
        test_model_DISALLOW_duplicate_name
        _check_model
    """

    def setUp(self):
        super().setUp()

    def _check_model(
        self,
        target_model,
        name,
        description,
        token_cost_per_1M_input,
        token_cost_per_1M_output,
        best_use_cases,
        access_mode,
        access_endpoint,
        max_tokens,
        user,
    ):
        """
        This function attempts a number of assertions against a Model

        args:

        returns:
        """
        self.assertEqual(target_model.name, name)
        self.assertEqual(target_model.description, description)
        self.assertAlmostEqual(
            float(target_model.token_cost_per_1M_input), float(token_cost_per_1M_input)
        )
        self.assertAlmostEqual(
            float(target_model.token_cost_per_1M_output),
            float(token_cost_per_1M_output),
        )
        self.assertEqual(target_model.best_use_cases, best_use_cases)
        self.assertEqual(target_model.access_mode, access_mode)
        self.assertEqual(target_model.access_endpoint, access_endpoint)
        self.assertEqual(target_model.max_tokens, max_tokens)
        self.assertEqual(target_model.created_by, user)
        self.assertEqual(target_model.created_at, date.today())

    def test_saving_and_retrieving_models(self):
        """
        This function tests creating a Model and then retrieving it.

        args:

        returns:
        """
        ai_model = create_ai_model(
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
        ai_model = create_ai_model(
            self.user1,
            "4.1",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )

        saved_models = AIModel.objects.all()
        first_saved_model = saved_models[0]
        second_saved_model = saved_models[1]

        self._check_model(
            first_saved_model,
            "4.1",
            "General-purpose coding and writing",
            0.1000,
            0.5000,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
            self.user1,
        )

        self._check_model(
            second_saved_model,
            "4o",
            "General-purpose coding and writing",
            0.1000,
            0.5000,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
            self.user1,
        )

    def test_modifying_model(self):
        """
        This function tests making changes to a Model

        args:

        returns:
        """
        ai_model = create_ai_model(
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

        saved_models = AIModel.objects.all()
        first_saved_model = saved_models[0]
        first_saved_model.description = "Changed value for description"
        first_saved_model.modified_by = self.user1
        first_saved_model.save()

        saved_models = AIModel.objects.all()
        first_saved_model = saved_models[0]
        self.assertEqual(first_saved_model.description, "Changed value for description")
        self.assertEqual(first_saved_model.modified_by, self.user1)
        self.assertEqual(first_saved_model.modified_at, date.today())

    def test_deleting_model(self):
        """
        This function tests deleting a Model

        args:

        returns:
        """
        ai_model = create_ai_model(
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

        saved_models = AIModel.objects.all()
        self.assertEqual(saved_models.count(), 1)
        first_saved_model = saved_models[0]
        first_saved_model.delete()

        saved_models = AIModel.objects.all()
        self.assertEqual(saved_models.count(), 0)

    def test_effect_of_deleting_user_on_model(self):
        """
        This function tests what happens to a Model if a user is deleted
        It should still exist in the database

        args:

        returns:
        """
        ai_model = create_ai_model(
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

        saved_models = AIModel.objects.all()
        self.assertEqual(saved_models.count(), 1)
        self.assertEqual(saved_models[0].created_by, self.user2)

        saved_users = get_user_model().objects.all()
        self.assertEqual(saved_users.count(), 2)
        self.user2.delete()
        saved_users = get_user_model().objects.all()
        self.assertEqual(saved_users.count(), 1)

        saved_models = AIModel.objects.all()
        self.assertEqual(saved_models.count(), 1)
        self.assertNotEqual(saved_models[0].created_by, self.user2)

    def test_model_DISALLOW_duplicate_name(self):
        ai_model = create_ai_model(
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
        ai_model.save()

        with self.assertRaises(ValidationError):
            test_model = AIModel(
                name=ai_model.name,
                description=ai_model.description,
                token_cost_per_1M_input=ai_model.token_cost_per_1M_input,
                token_cost_per_1M_output=ai_model.token_cost_per_1M_output,
                best_use_cases=ai_model.best_use_cases,
                access_mode=ai_model.access_mode,
                access_endpoint=ai_model.access_endpoint,
                created_by=self.user1,
                modified_by=self.user1,
            )
            test_model.full_clean()

    def test_model_generate_ai_response(self):
        ai_model = create_ai_model(
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
        ai_model.save()

        ai_response = ai_model.get_aimodel_response("What is the capital of France?")
        self.assertIn(
            "Paris",
            ai_response.choices[0].message.content,
            "The response from the AI model did not contain the expected text.",
        )
