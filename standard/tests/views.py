from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from standard.tests import utils as test_utils


class BaseViewTestMixin(object):
    """
    This is the base class View tests.

    properties:

    methods:
        setUp
        test_procedures_list_view_initial_setup
        test_procedures_list_view_with_anonymous_and_existing_users
    """

    view = None
    view_object_name = ""
    model = None
    template_name = None
    view_url = ""
    instance = None

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            email="junior@project.com",
            username="junior",
            password="testpass123",
            # Set-up other user fields. Examples below.
            # first_name="Junior",
            # last_name="Programmer",
        )
        self.senior_user = get_user_model().objects.create_user(
            email="senior@project.com",
            username="senior",
            password="testpass123",
            # Set-up other user fields. Examples below.
            # first_name="Junior",
            # last_name="Programmer",
        )

    def test_view_initial_setup(self):
        test_utils.check_view_setup(
            self,
            self.view,
            self.model,
            self.view_object_name,
            self.template_name,
        )

    def test_view_with_anonymous_and_existing_users(self):
        request = test_utils.generate_request("GET", self.view_url, AnonymousUser())
        response = (
            self.view.as_view()(request)
            if self.id_for_object_view is None
            else self.view.as_view()(request, pk=self.id_for_object_view)
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        request = test_utils.generate_request("GET", "procedures/", self.user1)
        response = (
            self.view.as_view()(request)
            if self.id_for_object_view is None
            else self.view.as_view()(request, pk=self.id_for_object_view)
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)


class BaseViewEditTestMixin(BaseViewTestMixin):
    """
    This is the base class View tests for generic edit views.

    properties:

    methods:
        setUp
        test_procedures_list_view_initial_setup
    """

    form = None

    def test_view_initial_setup(self):
        test_utils.test_view_setup(
            self,
            self.view,
            self.model,
            self.form,
            self.view_object_name,
            self.template_name,
        )
