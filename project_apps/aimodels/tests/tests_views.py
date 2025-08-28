"""This module unit tests the views for the models app.

It has the test cases:
    ListViewTest: Showing a list of Model model.
    DetailViewTest: Showing the details of an instance of Model model.
    CreateViewTest: Enabling the creation of an instance of Model model.
    UpdateViewTest Enabling the edit of an instance of Model model.
    DeleteViewTest Enabling the delete of an instance of Model model.
"""

from datetime import date
from http import HTTPStatus

from django.http.response import Http404
from django.test import TestCase, tag

from standard.tests import utils as test_utils
from standard.tests.utils import UserSetupMixin
from standard.tests.views import BaseViewEditTestMixin, BaseViewTestMixin

from project_apps.aimodels.models import AIModel

from project_apps.aimodels.forms import AIModelForm

from project_apps.aimodels.tests.tests_models import create_ai_model
from project_apps.aimodels.views import (
    AIModelCreateView,
    AIModelDeleteView,
    AIModelDetailView,
    AIModelListView,
    AIModelUpdateView,
)


@tag("view")
class ListViewTest(UserSetupMixin, BaseViewTestMixin, TestCase):
    """
    This class performs basic tests for the List View focused on Model

    Attributes:

    methods:
        BaseViewTestMixin
            setUp
            test_view_initial_setup
            test_view_with_anonymous_and_existing_users
        test_procedures_model_view_for_object_data
        test_procedures_model_view_for_object_data_empty
    """

    view = AIModelListView
    view_object_name = "aimodels"
    model = AIModel
    template_name = "aimodels/aimodels.html"
    view_url = "aimodels/"

    def setUp(self):
        super().setUp()
        # self.instance = create_model(self.user1, field1, field2, field3)
        self.view_url = f"{self.view_url}/"
        self.id_for_object_view = None

    def test_view_rendering(self):
        ai_model = create_ai_model(
            self.user2,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "openai_api",
            "https://openrouter.ai/api/v1",
            4096,
        )
        ai_model = create_ai_model(
            self.user2,
            "4.1",
            "General-purpose reasoning",
            0.1,
            0.2,
            "Fast completions and visual input understanding",
            "openai_api",
            "https://openrouter.ai/api/v1",
            4096,
        )

        request = test_utils.generate_request("GET", self.view_url, self.user1)
        model_list_view = test_utils.setup_view_request(self.view, request)

        model_list_view.object_list = model_list_view.get_queryset()

        context = model_list_view.get_context_data()
        response = model_list_view.render_to_response(context)
        response.render()
        self.assertContains(response, "AIUI - Models")
        self.assertContains(response, "AI models that are available for inference.")
        self.assertContains(response, "4.1")
        self.assertContains(response, "General-purpose reasoning")
        self.assertContains(response, "4o")
        self.assertContains(response, "General-purpose coding and writing")
        self.assertContains(
            response,
            f"Created: {date.today().strftime('%d/%m/%Y')} by tempstaff.",
        )
        self.assertTemplateUsed(self.template_name)

    def test_view_rendering_empty_list(self):
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        model_list_view = test_utils.setup_view_request(self.view, request)

        model_list_view.object_list = model_list_view.get_queryset()

        context = model_list_view.get_context_data()
        response = model_list_view.render_to_response(context)
        response.render()
        self.assertContains(response, "AIUI - Models")
        self.assertNotContains(
            response,
            f"Created: {date.today().strftime('%d/%m/%Y')} by junior.",
        )
        # self.assertContains(response, "THE TEXT FOR THE SAVE BUTTON")
        self.assertTemplateUsed(self.template_name)

    def test_model_list_view_for_object_data(self):
        ai_model = create_ai_model(
            self.user2,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "openai_api",
            "https://openrouter.ai/api/v1",
            4096,
        )

        request = test_utils.generate_request("GET", self.view_url, self.user1)
        model_list_view = test_utils.setup_view_request(self.view, request)

        data = model_list_view.get_queryset()
        self.assertTrue(data.exists())
        self.assertIn("4o", str(data[0]))

    def test_model_list_view_for_object_data_empty(self):
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        model_list_view = test_utils.setup_view_request(self.view, request)

        data = model_list_view.get_queryset()
        self.assertFalse(data.exists())


@tag("view")
class DetailViewTest(UserSetupMixin, BaseViewTestMixin, TestCase):
    """
    This class performs basic tests for the Detail View focused on Model

    Attributes:

    methods:
        BaseViewTestMixin
            setUp
            test_view_initial_setup
            test_view_with_anonymous_and_existing_users
        setUp
        test_model_detail_view_for_object_data
        test_model_detail_view_for_object_data_empty
        test_view_rendering
    """

    view = AIModelDetailView
    view_object_name = "aimodel"
    model = AIModel
    template_name = "aimodels/aimodels_detail.html"
    view_url = "aimodels/"

    def setUp(self):
        super().setUp()
        self.instance = create_ai_model(
            self.user2,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "openai_api",
            "https://openrouter.ai/api/v1",
            4096,
        )
        self.view_url = f"{self.view_url}{self.instance.id}/"
        self.id_for_object_view = self.instance.id

    def test_view_rendering(self):
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        model_detail_view = test_utils.setup_view_request(
            self.view, request, self.instance.id
        )

        data = model_detail_view.get_queryset()
        self.assertTrue(data.exists())

        model_detail_view.object = model_detail_view.get_object()
        self.assertEqual(model_detail_view.object.name, "4o")
        context = model_detail_view.get_context_data()
        response = model_detail_view.render_to_response(context)
        response.render()
        self.assertContains(response, " - Model Details")
        self.assertContains(response, "Details for AI Model:")
        self.assertContains(response, "4o")
        self.assertContains(response, "General-purpose coding and writing")
        self.assertContains(response, "Fast completions and visual input understanding")
        self.assertTemplateUsed(self.template_name)

    def test_model_detail_view_for_object_data(self):
        create_ai_model(
            self.user2,
            "4.1",
            "General-purpose reasoning",
            0.1,
            0.2,
            "Fast completions and visual input understanding",
            "openai_api",
            "https://openrouter.ai/api/v1",
            4096,
        )
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        model_detail_view = test_utils.setup_view_request(
            self.view, request, self.instance.id
        )

        data = model_detail_view.get_queryset()
        self.assertTrue(data.exists())

        ai_model = model_detail_view.get_object()
        test_utils.check_object(
            self,
            ai_model,
            attribute_tests={
                "name": "4o",
                "description": "General-purpose coding and writing",
                "best_use_cases": "Fast completions and visual input understanding",
            },
        )

    def test_model_detail_view_for_object_data_empty(self):
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        model_detail_view = test_utils.setup_view_request(self.view, request, 1)

        data = model_detail_view.get_queryset()
        self.assertTrue(data.exists())

        with self.assertRaises(Http404):
            model_detail_view.get_object()


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
        test_model_create_view_get
        test_model_create_view_adding_model_no_modelitems
        test_model_create_view_adding_model_with_modelitems
        test_model_create_view_DISALLOW_duplicate_fieldnottobeduplicated
        test_model_create_view_DISALLOW_duplicate_modelitem_fieldnottobeduplicated_same_model
        test_model_create_view_ALLOW_duplicate_modelitem_fieldnottobeduplicated_different_models
    """

    view = AIModelCreateView
    view_object_name = "aimodel"
    model = AIModel
    template_name = "aimodels/aimodels_create.html"
    view_url = "aimodels/create/"
    form = AIModelForm

    def setUp(self):
        super().setUp()
        self.instance = create_ai_model(
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
        self.id_for_object_view = None

    def test_model_create_view_rendering(self):
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        model_create_view = test_utils.setup_view_request(self.view, request)
        response = model_create_view.get(model_create_view.request)
        self.assertIsNone(model_create_view.object)
        self.assertListEqual(response.template_name, [self.template_name])
        self.assertIsInstance(response.context_data["form"], self.form)

        response.resolve_template(self.template_name)

        view_html = response.rendered_content
        self.assertIn("csrfmiddlewaretoken", view_html)
        self.assertIn(
            '<form class="pt-3" action="" method="post" id="form-container">',
            view_html,
        )
        # Expected snippets from the page html
        html_tests = [
            "Add New AI Model",
            "AI Model Name",
            "Is Active",
            "AI Model Description",
            "Best Use Cases",
            "Access Mode",
            "Access Endpoint",
            "Max Tokens",
            "Token Cost per 1M Input",
            "Token Cost per 1M Output",
        ]
        for html_test in html_tests:
            self.assertIn(
                html_test,
                view_html,
            )

    def test_model_create_view_adding_model(self):
        request = test_utils.generate_request(
            "POST",
            self.view_url,
            self.user1,
            data={
                "name": "4.1",
                "description": "description value",
                "access_mode": "openai_api",
                "access_endpoint": "https://openrouter.ai/api/v1",
                "token_cost_per_1M_input": 1.00,
                "token_cost_per_1M_output": 1.00,
                "best_use_cases": "best use cases value",
                "max_tokens": 4096,
                "is_active": True,
            },
        )
        model_create_view = test_utils.setup_view_request(self.view, request)

        response = model_create_view.post(
            model_create_view.request,
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        saved_models = self.model.objects.all()
        self.assertEqual(saved_models.count(), 2)
        view_saved_model = (
            saved_models[1] if saved_models[1].name == "4.1" else saved_models[0]
        )

        test_utils.check_object(
            self,
            view_saved_model,
            attribute_tests={
                "name": "4.1",
                "description": "description value",
                "access_mode": "openai_api",
                "access_endpoint": "https://openrouter.ai/api/v1",
                "token_cost_per_1M_input": "1.0000",
                "token_cost_per_1M_output": "1.0000",
                "best_use_cases": "best use cases value",
                "max_tokens": "4096",
                "is_active": True,
                "created_by": str(self.user1),
                "created_at": str(date.today()),
            },
        )

    def test_model_create_view_DISALLOW_model_no_name(self):
        request = test_utils.generate_request(
            "POST",
            self.view_url,
            self.user1,
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
            },
        )
        request.user = self.user1
        model_create_view = test_utils.setup_view_request(self.view, request)

        response = model_create_view.post(
            model_create_view.request,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context_data["form"].errors["name"],
            ["This field is required."],
        )
        self.assertInHTML(
            "<ul class='errorlist' id='id_name_error'><li>This field is required.</li></ul>",
            response.rendered_content,
        )

        saved_models = self.model.objects.all()
        self.assertEqual(saved_models.count(), 1, "Incorrect number of model")

    def test_model_create_view_DISALLOW_model_duplicate_fieldnottobeduplicated(self):
        request = test_utils.generate_request(
            "POST",
            self.view_url,
            self.user1,
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
            },
        )
        request.user = self.user1
        model_create_view = test_utils.setup_view_request(self.view, request)

        response = model_create_view.post(
            model_create_view.request,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context_data["form"].errors["name"],
            ["AI Model with this AI Model Name already exists."],
        )
        self.assertInHTML(
            "<ul class='errorlist' id='id_name_error'><li>AI Model with this AI Model Name already exists.</li></ul>",
            response.rendered_content,
        )

        saved_models = self.model.objects.all()
        self.assertEqual(saved_models.count(), 1, "Incorrect number of model")


@tag("view")
class UpdateViewTest(UserSetupMixin, BaseViewEditTestMixin, TestCase):
    """
    This class performs basic tests for the updating of models

    Attributes:

    methods:
        BaseViewTestMixin
            setUp
            test_view_with_anonymous_and_existing_users
        BaseViewEditTestMixin
            test_view_initial_setup
        test_model_update_view_get
        test_model_update_view_updating_model
        test_model_update_view_DISALLOW_model_duplicate_fieldnottobeduplicated
        test_model_update_view_updating_model_with_modelitems
        test_model_update_view_updating_model_with_extra_modelitem
        test_model_update_view_DISALLOW_model_duplicate_modelitem_fieldnottobeduplicated_same_model
        test_model_update_view_ALLOW_model_duplicate_modelitem_fieldnottobeduplicated_different_models
    """

    view = AIModelUpdateView
    view_object_name = "aimodel"
    model = AIModel
    template_name = "aimodels/aimodels_update.html"
    view_url = "aimodels/update/"
    form = AIModelForm

    def setUp(self):
        super().setUp()
        self.instance = create_ai_model(
            self.user2,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "openai_api",
            "https://openrouter.ai/api/v1",
            4096,
        )
        self.view_url = f"{self.view_url}{self.instance.id}/"
        self.id_for_object_view = self.instance.id

    def test_model_update_view_rendering(self):
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        model_update_view = test_utils.setup_view_request(
            AIModelUpdateView,
            request,
            object_for_test=self.instance.id,
        )

        response = model_update_view.get(model_update_view.request)
        self.assertEqual(model_update_view.object, self.instance)
        self.assertListEqual(response.template_name, [self.template_name])
        self.assertIsInstance(response.context_data["form"], self.form)

        response.resolve_template(self.template_name)

        view_html = response.rendered_content
        self.assertIn("csrfmiddlewaretoken", view_html)
        self.assertIn(
            '<form class="pt-3" action="" method="post" id="form-container">',
            view_html,
        )
        # self.assertIn('name="modelitem-0-ORDER"', view_html)
        self.assertIn("csrfmiddlewaretoken", view_html)
        self.assertIn(
            '<form class="pt-3" action="" method="post" id="form-container">',
            view_html,
        )
        # Expected snippets from the page html
        html_tests = [
            "Edit AI Model",
            "AI Model Name",
            "Is Active",
            "AI Model Description",
            "Best Use Cases",
            "Access Mode",
            "Access Endpoint",
            "Max Tokens",
            "Token Cost per 1M Input",
            "Token Cost per 1M Output",
        ]
        for html_test in html_tests:
            self.assertIn(
                html_test,
                view_html,
            )

    def test_model_update_view_updating_model(self):
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        model_update_view = test_utils.setup_view_request(
            self.view,
            request,
            object_for_test=self.instance.id,
        )
        response = model_update_view.get(model_update_view.request)

        request = test_utils.generate_request(
            "POST",
            self.view_url,
            self.user1,
            data={
                "id": self.instance.id,
                "name": "4o changed",
                "description": self.instance.description,
                "access_mode": self.instance.access_mode,
                "access_endpoint": self.instance.access_endpoint,
                "token_cost_per_1M_input": 1.00,
                "token_cost_per_1M_output": 1.00,
                "best_use_cases": self.instance.best_use_cases,
                "max_tokens": 4096,
                "is_active": True,
            },
        )
        model_update_view = test_utils.setup_view_request(
            self.view,
            request,
            object_for_test=self.instance.id,
        )

        response = model_update_view.post(
            request,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        saved_models = self.model.objects.all()
        self.assertEqual(saved_models.count(), 1)

        test_utils.check_object(
            self,
            saved_models[0],
            attribute_tests={
                "name": "4o changed",
                "description": self.instance.description,
                "best_use_cases": self.instance.best_use_cases,
                "created_by": str(self.user2),
                "created_at": str(date.today()),
                "modified_by": str(self.user1),
                "modified_at": str(date.today()),
            },
        )

    def test_model_update_view_DISALLOW_model_duplicate_name_nottobeduplicated(self):
        second_model = create_ai_model(
            self.user2,
            "4.1",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "openai_api",
            "https://openrouter.ai/api/v1",
            4096,
        )
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        model_update_view = test_utils.setup_view_request(
            self.view,
            request,
            object_for_test=second_model.id,
        )
        response = model_update_view.get(model_update_view.request)

        request = test_utils.generate_request(
            "POST",
            self.view_url,
            self.user1,
            data={
                "id": second_model.id,
                "name": self.instance.name,
                "description": second_model.description,
                "access_mode": second_model.access_mode,
                "access_endpoint": second_model.access_endpoint,
                "token_cost_per_1M_input": 1.00,
                "token_cost_per_1M_output": 1.00,
                "best_use_cases": second_model.best_use_cases,
                "max_tokens": 4096,
                "is_active": True,
            },
        )
        model_update_view = test_utils.setup_view_request(
            self.view,
            request,
            object_for_test=second_model.id,
        )

        response = model_update_view.post(
            request,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context_data["form"].errors["name"],
            ["AI Model with this AI Model Name already exists."],
        )
        self.assertInHTML(
            "<ul class='errorlist' id='id_name_error'><li>AI Model with this AI Model Name already exists.</li></ul>",
            response.rendered_content,
        )

        saved_models = self.model.objects.all()
        self.assertEqual(saved_models.count(), 2)

    def test_model_update_view_DISALLOW_model_no_name(self):
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        model_update_view = test_utils.setup_view_request(
            self.view,
            request,
            object_for_test=self.instance.id,
        )
        response = model_update_view.get(model_update_view.request)

        request = test_utils.generate_request(
            "POST",
            self.view_url,
            self.user1,
            data={
                "id": self.instance.id,
                "name": "",
                "description": self.instance.description,
                "access_mode": self.instance.access_mode,
                "access_endpoint": self.instance.access_endpoint,
                "token_cost_per_1M_input": 1.00,
                "token_cost_per_1M_output": 1.00,
                "best_use_cases": self.instance.best_use_cases,
                "max_tokens": 4096,
                "is_active": True,
            },
        )
        model_update_view = test_utils.setup_view_request(
            self.view,
            request,
            object_for_test=self.instance.id,
        )

        response = model_update_view.post(
            request,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            response.context_data["form"].errors["name"],
            ["This field is required."],
        )
        self.assertInHTML(
            "<ul class='errorlist' id='id_name_error'><li>This field is required.</li></ul>",
            response.rendered_content,
        )

        saved_models = self.model.objects.all()
        self.assertEqual(saved_models.count(), 1)


@tag("view")
class DeleteViewTest(UserSetupMixin, BaseViewEditTestMixin, TestCase):
    """
    This class performs basic tests for the creating lists

    Attributes:

    methods:
        test_model_delete_view_get
        test_model_delete_view_delete_model
    """

    view = AIModelDeleteView
    view_object_name = "aimodel"
    model = AIModel
    template_name = "aimodels/aimodels_delete.html"
    view_url = "aimodels/delete/"

    def setUp(self):
        super().setUp()
        self.instance = create_ai_model(
            self.user2,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "openai_api",
            "https://openrouter.ai/api/v1",
            4096,
        )
        self.view_url = f"{self.view_url}{self.instance.id}/"
        self.id_for_object_view = self.instance.id

    def test_model_delete_view_rendering(self):
        request = test_utils.generate_request("GET", self.view_url, self.user1)
        model_delete_view = test_utils.setup_view_request(
            self.view,
            request,
            object_for_test=self.instance.id,
        )

        response = model_delete_view.get(model_delete_view.request)
        self.assertEqual(model_delete_view.object, self.instance)
        self.assertListEqual(response.template_name, [self.template_name])

        response.resolve_template(self.template_name)

        view_html = response.rendered_content
        self.assertIn("csrfmiddlewaretoken", view_html)
        self.assertIn(
            '<form class="pt-3" action="" method="post" id="form-container">',
            view_html,
        )
        self.assertIn("csrfmiddlewaretoken", view_html)
        self.assertIn(
            '<form class="pt-3" action="" method="post" id="form-container">',
            view_html,
        )
        # Expected snippets from the page html
        html_tests = [
            "Delete AI Model",
            "4o",
            "General-purpose coding and writing",
        ]
        for html_test in html_tests:
            self.assertIn(
                html_test,
                view_html,
            )
        # self.assertIn('name="modelitem-0-ORDER"', view_html)

    def test_model_delete_view_delete_model(self):
        second_model = self.model.objects.all()
        request = test_utils.generate_request(
            "POST",
            self.view_url,
            self.user1,
        )
        model_delete_view = test_utils.setup_view_request(
            self.view,
            request,
            object_for_test=self.instance.id,
        )

        response = model_delete_view.post(
            request,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        saved_models = self.model.objects.all()
        self.assertEqual(saved_models.count(), 0)
