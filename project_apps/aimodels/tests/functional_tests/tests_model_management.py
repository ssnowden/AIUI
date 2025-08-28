"""Functional tests for managing modelss in the project.

    These represent a users journey in performing tasks related to modelss and their management.

    Test Cases:
        ModelManagementTest: The base testcase for all tests on the models
        app
        ModelManagementTestLists
        ModelManagementTestDetail
        ModelManagementTestCreate
        ModelManagementTestUpdate
        ModelManagementTestDelete

NOTE: The section below can be deleted once the forms are defined. Guidance for intial development
only.
Content:
    SECTION 1: Imports for the models models.
    SECTION 2: If any helper methods in models tests_models.py import these as
    well.
    SECTION 3: Lists for what should be seen on a specific page
    SECTION 4: Base test case for the  models app.
    SECTION 5: Test case for lists of Model.
    SECTION 6: Test case for detail pages of Model.
    SECTION 7: Test case for create of Model.
    SECTION 8: Test case for update of Model.
    SECTION 9: Test case for delete of Model.

Usage:
    Copy this file to the functional_tests folder in project_apps.
    Delete the functional_tests folder in this app (NOT the project_apps functional_tests folder).
    Now, just slowly work through the tests modifying them for the apps needs.
    This may be the standard approach as laid out in the intial test formulations, or there may be
    a more recent set of user journeys to develop the tests for.
"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase, override_settings, tag
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from standard.tests.selenium import SeleniumMixin

""" SECTION 1 """
from project_apps.aimodels.models import AIModel
from project_apps.aimodels.tests.tests_models import create_ai_model

""" SECTION 3 """
# Checks lists for the basics on each page
CHECK_MODEL_LIST = [
    "Welcome to Your AI Models",
    "AI models that are available for inference.",
]
CHECK_MODEL_DETAIL = [
    "Details for AI Model:",
    "Edit AI Model",
    "Delete AI Model",
    "Description",
    "Best Use Cases",
    "Access Mode",
    "Access Endpoint",
    "Max Tokens",
    "Token Cost per 1M Input",
    "Token Cost per 1M Output",
    "Back to AI Models",
]
CHECK_MODEL_CREATE = [
    "Add New",
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
CHECK_MODEL_EDIT = [
    "Edit AI Model",
    "AI Model Name",
    "AI Model Description",
    "Best Use Cases",
    "Access Mode",
    "Access Endpoint",
    "Max Tokens",
    "Token Cost per 1M Input",
    "Token Cost per 1M Output",
]
CHECK_MODEL_DELETE = [
    "Delete AI Model",
    "4o",
    "General-purpose coding and writing",
]


class AIModelManagementTest(SeleniumMixin, LiveServerTestCase):
    """
    The base class for tests about a user performing Model management actions

    Attributes:

    methods:
        SeleniumMixin
            user_login
            _set_up_web_driver
            _tear_down_web_driver
            _data_entry
            _scroll_to_element_id_and_click
        setUpClass
        tearDownClass
        setUp
        _test_click_add_modelitem_form_fails
        _go_to_model_list
        _check_in_page
        _check_not_in_page
        _add_modelitem
        _check_elements_values
    """

    host = "0.0.0.0"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._set_up_web_driver()

    @classmethod
    def tearDownClass(cls):
        cls._tear_down_web_driver()
        super().tearDownClass()

    def _test_click_add_modelitem_form_fails(self):
        with self.assertRaises(
            ElementClickInterceptedException,
            msg="Allowing addition of form when shouldn't be",
        ):
            self.selenium.find_element_by_id("add-ModelItem-form").click()

    def _go_to_model_list(self):
        # The user has signed up, goes to the home page
        self.selenium.get(self.live_server_url)
        # logs in
        self.user_login(self.senior_user.email, "testpass123")
        self.selenium.implicitly_wait(5)
        # and is now at the home page
        self.assertIn("Home - ", self.selenium.title)
        self.assertIn(
            "Models",
            self.selenium.page_source,
        )

        # They then click on the Model link to go to the list page.
        self._scroll_to_element_id_and_click("sidebar-toggler")
        self.selenium.implicitly_wait(5)
        self._scroll_to_element_id_and_click("aimodels")

    def _add_modelitem(self, num_items, start_range=0, add_to_item_number=0):
        for item_number in range(start_range, start_range + num_items):
            self._data_entry(
                f"id_ModelItem-{item_number}-text",
                f"ModelItem {item_number+add_to_item_number}",
            )
            self._data_entry(f"id_ModelItem-{item_number}-when", "9am")
            item_order_box = self.selenium.find_element_by_id(
                f"id_ModelItem-{item_number}-ORDER"
            )
            self.assertEqual(
                item_order_box.get_attribute("value"), str(item_number + 1)
            )
            self._scroll_to_element_id_and_click("add-ModelItem-form")

    def _check_elements_values(self, elements_to_be_checked):
        for element, value in elements_to_be_checked.items():
            item_input = self.selenium.find_element_by_id(element)
            self.assertEqual(item_input.get_attribute("value"), value)


@tag("selenium")
@override_settings(ALLOWED_HOSTS=["*"])
@override_settings(SECURE_SSL_REDIRECT=False)
@override_settings(CSRF_COOKIE_SECURE=False)
@override_settings(SESSION_COOKIE_SECURE=False)
class AIModelManagementTestLists(AIModelManagementTest):
    """
    This class makes tests about a user looking at lists of Models

    Attributes:

    methods:
        SeleniumMixin
            user_login
            _set_up_web_driver
            _tear_down_web_driver
            _data_entry
            _scroll_to_element_id_and_click
        ModelManagementTest
            setUpClass
            tearDownClass
            setUp
            _test_click_add_modelitem_form_fails
            _go_to_model_list
            _check_in_page
            _check_not_in_page
            _add_modelitem
            _check_elements_values
        test_view_lists
        test_view_lists_empty
        test_view_lists_not_logged_in
    """

    def test_view_lists(self):
        """
        This function tests the ability of an existing user to view any existing lists
        of Model.

        preconditions:
            A user with an account.
            Two models already existing to form a list

        results:
            User can see a list of models that are available.
        """
        ai_model = create_ai_model(
            self.senior_user,
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
            self.senior_user,
            "4.1",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )
        self._go_to_model_list()

        # Now on the list page the user can see the requisite list of Models
        self.assertIn("AIUI - Models", self.selenium.title)
        self._check_in_page(CHECK_MODEL_LIST)
        # displaying currently available lists
        self._check_in_page(
            [
                "4.1",
                "4o",
            ]
        )

    def test_view_lists_empty(self):
        """
        This function tests an existing user viewing any existing lists when there
        are none

        preconditions:
            A user with an account.

        results:
            User can see a message that there are no lists available.
        """
        self._go_to_model_list()

        # Now on the list page the user can see there are no Models
        self.assertIn("AIUI - Models", self.selenium.title)
        # displaying currently available lists
        self.assertIn(
            "Add your first AI model",
            self.selenium.page_source,
        )

    def test_view_lists_not_logged_in(self):
        """
        This function tests that the list of Models requires a user to be logged in

        preconditions:
            Trying to access Model list page but not logged in

        results:
            Tring to view the Model list without being logged in will require a login.
        """
        # A user not logged in goes directly to the Model list page
        self.selenium.get(f"{self.live_server_url}/aimodels/")
        # ...due to the fact they are not logged in redirected to the login page
        self.assertIn(
            "Login",
            self.selenium.page_source,
        )
        self.user_login("senior@project.com", "testpass123")
        self.selenium.implicitly_wait(5)
        # After login find themselves at the Model list page.
        self.assertIn("AIUI - Models", self.selenium.title)


@tag("selenium")
@override_settings(ALLOWED_HOSTS=["*"])
@override_settings(SECURE_SSL_REDIRECT=False)
@override_settings(CSRF_COOKIE_SECURE=False)
@override_settings(SESSION_COOKIE_SECURE=False)
class AIModelManagementTestDetail(AIModelManagementTest):
    """
    This class makes tests about a user viewing the details of an instance of
    Model.

    Attributes:

    methods:
        SeleniumMixin
            user_login
            _set_up_web_driver
            _tear_down_web_driver
            _data_entry
            _scroll_to_element_id_and_click
        ModelManagementTest
            setUpClass
            tearDownClass
            setUp
            _test_click_add_modelitem_form_fails
            _go_to_model_list
            _check_in_page
            _check_not_in_page
            _add_modelitem
            _check_elements_values
        test_view_model_detail
        test_view_model_detail_not_logged_in
    """

    def test_model_view_detail(self):
        """
        This function tests an existing user viewing the details of an instance
        of Model.

        preconditions:
            A user with an account.
            a list in the db

        results:
            User can see a the details of the list.
        """
        # Two lists already exist
        ai_model = create_ai_model(
            self.senior_user,
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
            self.senior_user,
            "4.1",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )

        self._go_to_model_list()

        # This takes them to the list page displaying currently available lists
        # So they click on the first one to see it's details.
        self._scroll_to_element_id_and_click(ai_model.name)
        self.assertIn("AIUI - Model Details", self.selenium.title)
        self._check_in_page(CHECK_MODEL_DETAIL)

        # ...and are able to see various details for that list.
        self._check_in_page(
            [
                "4o",
                "Model is active",
                ai_model.description,
                ai_model.best_use_cases,
                ai_model.access_mode,
                ai_model.access_endpoint,
                ai_model.max_tokens,
                ai_model.token_cost_per_1M_input,
                ai_model.token_cost_per_1M_output,
            ]
        )

    def test_view_model_detail_not_logged_in(self):
        """
        This function tests that viewing the detail of a model
        requires a user to be logged in

        preconditions:
            Trying to access model detail page but not logged in
            A list in the DB

        results:
            Tring to view the procedures detail without being logged in will require a login.
        """
        # A model already exist
        ai_model = create_ai_model(
            self.senior_user,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )

        self.selenium.get(f"{self.live_server_url}/aimodels/{ai_model.id}/")
        self.assertIn(
            "Login",
            self.selenium.page_source,
        )
        self.user_login("senior@project.com", "testpass123")
        self.selenium.implicitly_wait(5)
        self.assertIn("AIUI - Model Details", self.selenium.title)


@tag("selenium")
@override_settings(ALLOWED_HOSTS=["*"])
@override_settings(SECURE_SSL_REDIRECT=False)
@override_settings(CSRF_COOKIE_SECURE=False)
@override_settings(SESSION_COOKIE_SECURE=False)
class AIModelManagementTestCreate(AIModelManagementTest):
    """
    This class makes tests about a user performing Model creation actions

    Attributes:

    methods:
        SeleniumMixin
            user_login
            _set_up_web_driver
            _tear_down_web_driver
            _data_entry
            _scroll_to_element_id_and_click
        ModelManagementTest
            setUpClass
            tearDownClass
            setUp
            _test_click_add_modelitem_form_fails
            _go_to_model_list
            _check_in_page
            _check_not_in_page
            _add_modelitem
            _check_elements_values
        _go_to_create
        _add_base_fields
        test_view_model_create
        test_view_model_create_DISALLOW_multiple_add_modelitem_form_clicks
        test_view_model_create_add_modelitem_form_ordering
        test_view_model_create_modelitem_changing_order
        test_view_model_create_delete_extra_modelitem_form_from_model
        test_view_model_create_delete_extra_modelitem_form_with_fieldvalue_entered_from_model
        test_view_model_create_no_requiredfield
        test_view_model_create_no_duplicate_fieldnottobeduplicated
        test_view_model_create_no_duplicate_modelitem_fieldnottobeduplicated_for_same_model
        test_view_model_create_CAN_duplicate_modelitem_fieldnottobeduplicated_for_different_model
        test_view_model_create_not_logged_in
    """

    def _go_to_create(self):
        # User clicks on the create link to add a new list.
        self._scroll_to_element_id_and_click("create-model")

    def _add_base_fields(self):
        self._data_entry("id_name", "4o")
        self._data_entry("id_description", "General-purpose coding and writing")
        self._data_entry(
            "id_best_use_cases", "Fast completions and visual input understanding"
        )
        self._data_entry("id_access_endpoint", "https://openrouter.ai/api/v1")

    def test_view_model_create(self):
        """
        This function tests an existing user creating a model
        with modelitem.

        preconditions:
            A user with an account.

        results:
            User can see the list detail page with the details for the list they just
            created.
        """
        self._go_to_model_list()
        # This takes them to the list page
        # displaying currently available models
        # Now the user clicks on create model
        self._go_to_create()
        self.assertIn("AIUI - Models Creation", self.selenium.title)
        # ...and are able to see various details for creating a list.
        self._check_in_page(CHECK_MODEL_CREATE)
        # Now they add the base fields for a Model.
        self._add_base_fields()
        # Clicks save
        self._scroll_to_element_id_and_click("id-save-model")
        # and can see they are in the detail page
        self.assertIn("AIUI - Model Details", self.selenium.title)
        # ...and are able to see various details for that list.
        # and they are the same as the ones inputed in creation
        self._check_in_page(
            [
                "4o",
                "Model is active",
                "General-purpose coding and writing",
                "Fast completions and visual input understanding",
                "openai_api",
                "https://openrouter.ai/api/v1",
                "4096",
                "0.0000",
            ]
        )

    def test_view_model_create_no_requiredfield(self):
        """
        This function tests an existing user trying to create a model without a requiredfield.

        preconditions:
            A user with an account.

        results:
            User can see the list create page with the details for the list they just
            created and an error message - "Please fill out this field."
        """
        self._go_to_model_list()
        # taking them to the list page
        # displaying currently available lists

        self._go_to_create()
        self.assertIn("AIUI - Models Creation", self.selenium.title)

        # Then adds a description but no name for the List
        self._data_entry("id_description", "General-purpose coding and writing")
        self._data_entry(
            "id_best_use_cases", "Fast completions and visual input understanding"
        )
        self._data_entry("id_access_endpoint", "https://openrouter.ai/api/v1")

        # Then clicks save
        self._scroll_to_element_id_and_click("id-save-model")

        # but sees that they are still on the model creation page
        self.assertIn("AIUI - Models Creation", self.selenium.title)

        # ...with a message to fill out the requiredfield - change requiredfield to the field details that is required in all parts of the following code.
        # such that input#id_requiredfield[name='requiredfield'] becomes e.g. input#id_description[name='description']
        validation_message = (
            WebDriverWait(self.selenium, 20)
            .until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "input#id_name[name='name']")
                )
            )
            .get_attribute("validationMessage")
        )

        self.assertIn("Please fill out this field.", validation_message)

    def test_view_model_create_no_duplicate_name_nottobeduplicated(self):
        """
        This function tests an existing user trying to create a model with a fieldnottobeduplicated
        that already exists for an existing model

        preconditions:
            A user with an account.
            An existing model

        results:
            User can see the list create page with the details for the list they just
            created and an error message - "The name for this list already exists"
        """
        # Given a model already exists
        ai_model = create_ai_model(
            self.senior_user,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )
        self._go_to_model_list()
        # taking them to the list page
        # displaying currently available models

        self._go_to_create()
        self.assertIn("AIUI - Models Creation", self.selenium.title)

        self._add_base_fields()

        # Then clicks save
        self._scroll_to_element_id_and_click("id-save-model")

        # but sees that they are still on the list creation page
        self.assertIn("AIUI - Models Creation", self.selenium.title)

        # ...with the various details for that model.
        self._check_in_page(
            [
                "AI Model with this AI Model Name already exists.",
            ]
        )

    def test_view_model_create_not_logged_in(self):
        """
        This function tests that the create model view requires a user to be logged in

        preconditions:
            Trying to access model create but not logged in

        results:
            Trying to view the model create without being logged in will require a login.
        """
        self.selenium.get(f"{self.live_server_url}/aimodels/create/")
        self.assertIn(
            "Login",
            self.selenium.page_source,
        )
        self.user_login("senior@project.com", "testpass123")
        self.selenium.implicitly_wait(5)
        self.assertIn("AIUI - Models Creation", self.selenium.title)


@tag("selenium")
@override_settings(ALLOWED_HOSTS=["*"])
@override_settings(SECURE_SSL_REDIRECT=False)
@override_settings(CSRF_COOKIE_SECURE=False)
@override_settings(SESSION_COOKIE_SECURE=False)
class AIModelManagementTestUpdate(AIModelManagementTest):
    """
    This class makes tests about a user performing list update actions

    Attributes:

    methods:
        SeleniumMixin
            user_login
            _set_up_web_driver
            _tear_down_web_driver
            _data_entry
            _scroll_to_element_id_and_click
        ModelManagementTest
            setUpClass
            tearDownClass
            setUp
            _test_click_add_modelitem_form_fails
            _go_to_model_list
            _check_in_page
            _check_not_in_page
            _add_modelitem
            _check_elements_values
        test_view_model_update_model_basefields
        test_view_model_update_no_requiredfield
        test_view_model_update_no_duplicate_fieldnottobeduplicated
        test_view_model_update_NO_duplicate_modelitem_fieldnottobeduplicated_for_same_model
        test_view_model_update_add_new_modelitem_to_model
        test_view_model_update_DISALLOW_multiple_add_modelitem_form_clicks
        test_view_model_update_add_modelitem_form_ordering
        test_view_model_update_add_new_modelitem_to_model_changing_order
        test_view_model_update_delete_existing_modelitem_from_model
        test_view_model_update_delete_extra_modelitem_form_from_model
        test_view_model_update_delete_extra_modelitem_form_with_text_entered_from_model
        test_view_model_update_CAN_duplicate_modelitem_fieldnottobeduplicated_for_different_model
        test_view_model_update_not_logged_in
    """

    def _go_to_edit(self, model):
        self._scroll_to_element_id_and_click(model.name)
        self.assertIn("AIUI - Model Details", self.selenium.title)

        self._scroll_to_element_id_and_click("edit-aimodel")

    def test_view_model_update_model_basefields(self):
        """
        This function tests an existing user updating the basefields of a model
        without modelitem.

        preconditions:
            A user with an account.
            a model already saved to the database.

        results:
            User can see the model detail page with the details for the model they just
            updated.
        """
        # A model already exists.
        ai_model = create_ai_model(
            self.senior_user,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )

        self._go_to_model_list()
        # This takes them to the model list page
        # displaying currently available models

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(ai_model)
        self.assertIn("AIUI - Model Update", self.selenium.title)

        # .. and can see they are in the edit page
        self._check_in_page(CHECK_MODEL_EDIT)

        # ...and are able to see various details of the list ready for changing.
        self._check_in_page(
            [
                "4o",
                "General-purpose coding and writing",
                "Fast completions and visual input understanding",
            ]
        )

        # Now they add the name and description for the List
        self._data_entry("id_name", "name has changed")
        self._data_entry("id_description", "description has changed")

        # Clicks update
        self._scroll_to_element_id_and_click("id-save-model")

        # and can see the item that they created
        self.assertIn("AIUI - Model Details", self.selenium.title)

        # ...and are able to see various details for that list.
        # and they are the same as the ones inputted at update
        self._check_in_page(
            [
                "name has changed",
                "description has changed",
                "Fast completions and visual input understanding",
            ]
        )

    def test_view_model_update_no_requiredfield(self):
        """
        This function tests an existing user trying to update a model without a requiredfield.

        preconditions:
            An existing model
            A user with an account.

        results:
            User can see the model update page with the details for the model they just
            updated and an error message - "Please fill out this field."
        """
        # A model already exists.
        ai_model = create_ai_model(
            self.senior_user,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )

        self._go_to_model_list()
        # This takes them to the model list page
        # displaying currently available models

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(ai_model)
        self.assertIn("AIUI - Model Update", self.selenium.title)

        # .. and can see they are in the edit page
        self._check_in_page(CHECK_MODEL_EDIT)

        # ...and are able to see various details of the list ready for changing.
        self._check_in_page(
            [
                "4o",
                "General-purpose coding and writing",
                "Fast completions and visual input understanding",
            ]
        )

        # Now they add the name and description for the List
        self._data_entry("id_name", "")
        self._data_entry("id_description", "description has changed")

        # Clicks update
        self._scroll_to_element_id_and_click("id-save-model")

        # but sees that they are still on the list update page
        self.assertIn("AIUI - Model Update", self.selenium.title)

        validation_message = (
            WebDriverWait(self.selenium, 20)
            .until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "input#id_name[name='name']")
                )
            )
            .get_attribute("validationMessage")
        )
        # with an error message
        self.assertIn("Please fill out this field.", validation_message)

    def test_view_model_update_no_duplicate_fieldnottobeduplicated(self):
        """
        This function tests an existing user trying to update a model with a fieldnottobeduplicated
        that already exists for an existing model

        preconditions:
            A user with an account.
            Two existing models

        results:
            User can see the model update page with the details for the model they just
            updated and an error message - "The fieldnottobeduplicated for this model already exists"
        """
        # Given two models already exists.
        ai_model = create_ai_model(
            self.senior_user,
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
            self.senior_user,
            "4.1",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )

        self._go_to_model_list()
        # This takes them to the model list page
        # displaying currently available models

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(ai_model)
        self.assertIn("AIUI - Model Update", self.selenium.title)

        # .. and can see they are in the edit page
        self._check_in_page(CHECK_MODEL_EDIT)

        # ...and are able to see various details of the list ready for changing.
        self._check_in_page(
            [
                "4o",
                "General-purpose coding and writing",
                "Fast completions and visual input understanding",
            ]
        )

        # Now they add the name and description for the List
        self._data_entry("id_name", "4.1")

        # Clicks update
        self._scroll_to_element_id_and_click("id-save-model")

        # but sees that they are still on the list update page
        self.assertIn("AIUI - Model Update", self.selenium.title)

        # ...with the various details for that list.
        self._check_in_page(
            [
                "4.1",
                "General-purpose coding and writing",
                # and an error message
                "AI Model with this AI Model Name already exists.",
            ]
        )

    def test_view_model_update_not_logged_in(self):
        """
        This function tests that the update model view requires a user to be logged in

        preconditions:
            Trying to access /model/update but not logged in

        results:
            Trying to view the model update without being logged in will require a login.
        """
        # A model already exists.
        ai_model = create_ai_model(
            self.senior_user,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )

        self.selenium.get(f"{self.live_server_url}/aimodels/update/{ai_model.id}/")
        self.assertIn(
            "Login",
            self.selenium.page_source,
        )
        self.user_login("senior@project.com", "testpass123")
        self.selenium.implicitly_wait(5)
        self.assertIn("AIUI - Model Update", self.selenium.title)
        self.assertIn(
            "4o",
            self.selenium.page_source,
        )


@tag("selenium")
@override_settings(ALLOWED_HOSTS=["*"])
@override_settings(SECURE_SSL_REDIRECT=False)
@override_settings(CSRF_COOKIE_SECURE=False)
@override_settings(SESSION_COOKIE_SECURE=False)
class AIModelManagementTestDelete(AIModelManagementTest):
    """
    This class makes tests about a user performing Model delete actions

    Attributes:

    methods:
        SeleniumMixin
            user_login
            _set_up_web_driver
            _tear_down_web_driver
            _data_entry
            _scroll_to_element_id_and_click
        ModelManagementTest
            setUpClass
            tearDownClass
            setUp
            _test_click_add_modelitem_form_fails
            _go_model_list
            _check_in_page
            _check_not_in_page
            _add_modelitem
            _check_elements_values
        test_view_model_delete_not_logged_in
        test_view_model_delete_model
    """

    def test_view_model_delete_not_logged_in(self):
        """
        This function tests that the delete model view requires a user to be logged in

        preconditions:
            models already exist
            Trying to access /model/delete but not logged in

        results:
            Trying to view the model delete without being logged in will require a login.
        """
        # A model already exists.
        ai_model = create_ai_model(
            self.senior_user,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )

        self.selenium.get(f"{self.live_server_url}/aimodels/delete/{ai_model.id}/")
        self.assertIn(
            "Login",
            self.selenium.page_source,
        )
        self.user_login("senior@project.com", "testpass123")
        self.selenium.implicitly_wait(5)
        self.assertIn("AIUI - Model Delete", self.selenium.title)
        self.assertIn(
            "4o",
            self.selenium.page_source,
        )

    def test_view_model_delete_model(self):
        """
        This function tests an existing user deleting a model

        preconditions:
            A user with an account.
            a model already saved to the database.

        results:
            User can see the model procedures page without the details for the model they just
            deleted.
        """
        # A model already exists.
        ai_model = create_ai_model(
            self.senior_user,
            "4o",
            "General-purpose coding and writing",
            0.1,
            0.5,
            "Fast completions and visual input understanding",
            "OpenAI API",
            "https://openrouter.ai/api/v1",
            4096,
        )

        self._go_to_model_list()
        # This takes them to the model list page
        # displaying currently available models

        # So they click on the first one to see it's details.
        self._scroll_to_element_id_and_click(ai_model.name)
        self.assertIn("AIUI - Model Details", self.selenium.title)

        # They see that there is a list that needs deleting so click delete
        self._scroll_to_element_id_and_click("delete-aimodel")
        self.assertIn("AIUI - Model Delete", self.selenium.title)
        self._check_in_page(CHECK_MODEL_DELETE)

        # ...and are able to see various details of the list ready for deleting.
        self._check_in_page(
            [
                "4o",
            ]
        )

        # Clicks delete
        self._scroll_to_element_id_and_click("id-delete-model")

        # This takes them to the list page
        self.assertIn("AIUI - Models", self.selenium.title)
        # displaying currently available model
        self.assertIn(
            "Add your first AI model",
            self.selenium.page_source,
        )
