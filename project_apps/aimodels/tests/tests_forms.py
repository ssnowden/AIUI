"""This module unit tests the views for the models app.

It has the test cases:
    CreateModelFormTest:
    CreateModelItemFormTest:
    CreateModelItemFormsetTest:
    UpdateModelFormTest:
    UpdateModelItemFormTest:
    UpdateModelItemFormsetTest:
"""

import html

from django.test import TestCase, tag

from standard.tests.utils import UserSetupMixin

from project_apps.aimodels.forms import AIModelForm

from project_apps.aimodels.tests.tests_models import create_ai_model


@tag("form")
class CreateModelFormTest(UserSetupMixin, TestCase):
    """
    This class performs basic tests for the Model Create Form.

    Attributes:

    methods:
        setUp
        test_create_model_form_html
        test_create_model_form_validation_blank_fields
        test_create_model_form_validation_ok
        test_create_model_form_for_duplicate_model_fieldnottobeduplicated

    """

    def setUp(self):
        super().setUp()

    def test_create_model_form_html(self):
        form = AIModelForm()

        form_html = form.as_p()

        self.assertFalse(form.is_bound)
        self.assertNotIn("AI Model Created By", form_html)
        self.assertNotIn("AI Model Modified By", form_html)
        self.assertIn("AI Model Name", form_html)
        self.assertIn("AI Model Description", form_html)
        self.assertIn("Access Mode", form_html)
        self.assertIn("openai_api", form_html)
        self.assertIn("local", form_html)
        self.assertIn("openrouter", form_html)
        self.assertIn("transformer", form_html)
        self.assertIn("Access Endpoint", form_html)
        self.assertIn("Token Cost per 1M Input", form_html)
        self.assertIn("Token Cost per 1M Output", form_html)
        self.assertIn("Best Use Cases", form_html)
        self.assertIn("Max Tokens", form_html)
        self.assertIn("Is Active", form_html)

    def test_create_model_form_validation_ok(self):
        form = AIModelForm(
            data={
                "name": "name value",
                "description": "description value",
                "access_mode": "openai_api",
                "access_endpoint": "https://openrouter.ai/api/v1",
                "token_cost_per_1M_input": 1.00,
                "token_cost_per_1M_output": 1.00,
                "best_use_cases": "best use cases value",
                "max_tokens": 4096,
                "is_active": True,
            }
        )
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
        self.assertDictEqual(form.errors, {})

    def test_create_model_form_validation_blank_fields(self):
        form = AIModelForm(
            data={
                "name": "",
                "description": "description value",
                "access_mode": "openai_api",
                "access_endpoint": "https://openrouter.ai/api/v1",
                "token_cost_per_1M_input": 1.00,
                "token_cost_per_1M_output": 1.00,
                "best_use_cases": "best use cases value",
                "max_tokens": 4096,
                "is_active": True,
            }
        )
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {
                "name": ["This field is required."],
            },
        )

    def test_create_model_form_for_duplicate_model_field_name_nottobeduplicated(self):
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
        form = AIModelForm(
            data={
                "name": "4o",
                "description": "description value",
                "access_mode": "openai_api",
                "access_endpoint": "https://openrouter.ai/api/v1",
                "token_cost_per_1M_input": 1.00,
                "token_cost_per_1M_output": 1.00,
                "best_use_cases": "best use cases value",
                "max_tokens": 4096,
                "is_active": True,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["name"],
            ["AI Model with this AI Model Name already exists."],
        )


@tag("form")
class UpdateModelFormTest(UserSetupMixin, TestCase):
    """
    This class performs basic tests for the List Update Form.

    Attributes:

    methods:
        setUp
        test_update_model_form_html
        test_update_model_form_validation_blank_fields
        test_update_model_form_validation_ok
        test_update_model_form_for_duplicate_list_name

    """

    def setUp(self):
        super().setUp()
