"""This module performs integration tests the models app ensuring all aspects
    of the apps development work together.

It has the test case:
    AIModelTest: This ensures that the AI Model can be accessed appropriately.

"""

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings, tag
from django.urls import reverse

from standard.tests.utils import UserSetupMixin

""" SECTION 1 """
from project_apps.aimodels.models import AIModel
from project_apps.aimodels.tests.tests_models import create_ai_model


@tag("integration")
@override_settings(SECURE_SSL_REDIRECT=False)
class AIModelTest(UserSetupMixin, TestCase):
    """
    This class performs basic tests of the models app

    Attributes:

    methods:
        setUp
        test_views_of_model_not_logged_in
        test_views_logged_in
    """

    def _get_response(self, user=None, url=None):
        if user is not None:
            self.client.force_login(user)

        return self.client.get(url, follow=True)

    def test_views_of_model_not_logged_in(self):
        """
        This function tests that the response for all model
        views without a user being logged in.

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
        create_ai_model(
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

        response = self._get_response(url=reverse("aimodels"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Login")

        response = self._get_response(
            url=reverse("aimodel_detail", kwargs={"pk": ai_model.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Login")

        response = self.client.get(reverse("aimodel_create"), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Login")

        response = self.client.get(
            reverse("aimodel_update", kwargs={"pk": ai_model.id}), follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Login")

        response = self.client.get(
            reverse("aimodel_delete", kwargs={"pk": ai_model.id}), follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Login")

    def test_views_logged_in(self):
        """
        This function tests a view where there are no existing model.

        args:

        returns:
        """
        response = self._get_response(self.user1, reverse("aimodels"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "AIUI - Models")
        self.assertTemplateUsed("aimodels/aimodels.html")
        self.assertTemplateUsed("aimodels/list/aimodels_list_empty.html")

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
        create_ai_model(
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
        response = self._get_response(self.user1, reverse("aimodels"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "AIUI - Models")
        self.assertContains(response, "4o")
        self.assertContains(response, "4.1")
        self.assertTemplateUsed("aimodels/aimodels.html")
        self.assertTemplateUsed("aimodels/list/aimodels_list.html")
        self.assertTemplateUsed("aimodels/list/aimodels_list_header.html")
        self.assertTemplateUsed("aimodels/list/aimodels_list_title.html")
        self.assertTemplateUsed("aimodels/list/aimodels_list_item.html")

        response = self._get_response(self.user1, ai_model.get_absolute_url())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "AIUI - Model Details")
        self.assertContains(response, "Details for AI Model:")
        self.assertContains(response, "40")
        self.assertContains(response, "General-purpose coding and writing")
        self.assertTemplateUsed("aimodels/aimodels_detail.html")
        self.assertTemplateUsed("aimodels/detail/aimodels_detail_item.html")
        self.assertTemplateUsed("aimodels/detail/aimodels_detail_header.html")

        response = self._get_response(self.user1, reverse("aimodel_create"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "AIUI - Models Creation")
        self.assertContains(response, "Add New AI Model")
        self.assertTemplateUsed("aimodels/aimodels_create.html")
        self.assertTemplateUsed("aimodels/detail/aimodels_form.html")

        response = self._get_response(
            self.user1,
            reverse("aimodel_update", kwargs={"pk": ai_model.id}),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "AIUI - Model Update")
        self.assertContains(response, "Edit AI Model")
        self.assertTemplateUsed("aimodels/aimodels_update.html")
        self.assertTemplateUsed("aimodels/detail/aimodels_form.html")

        response = self._get_response(
            self.user1,
            reverse("aimodel_delete", kwargs={"pk": ai_model.id}),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "AIUI - Model Delete")
        self.assertContains(response, "Delete AI Model")
        self.assertTemplateUsed("aimodels/aimodels_delete.html")
