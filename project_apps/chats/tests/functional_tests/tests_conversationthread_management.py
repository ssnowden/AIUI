"""Functional tests for managing chatss in the project.

    These represent a users journey in performing tasks related to chatss and their management.

    Test Cases:
        ConversationThreadManagementTest: The base testcase for all tests on the chats
        app
        ConversationThreadManagementTestLists
        ConversationThreadManagementTestDetail
        ConversationThreadManagementTestCreate
        ConversationThreadManagementTestUpdate
        ConversationThreadManagementTestDelete

NOTE: The section below can be deleted once the forms are defined. Guidance for intial development
only.
Content:
    SECTION 1: Imports for the chats models.
    SECTION 2: If any helper methods in chats tests_models.py import these as
    well.
    SECTION 3: Lists for what should be seen on a specific page
    SECTION 4: Base test case for the  chats app.
    SECTION 5: Test case for lists of ConversationThread.
    SECTION 6: Test case for detail pages of ConversationThread.
    SECTION 7: Test case for create of ConversationThread.
    SECTION 8: Test case for update of ConversationThread.
    SECTION 9: Test case for delete of ConversationThread.

Usage:
    Copy this file to the functional_tests folder in project_apps.
    Delete the functional_tests folder in this app (NOT the project_apps functional_tests folder).
    Now, just slowly work through the tests modifying them for the apps needs.
    This may be the standard approach as laid out in the intial test formulations, or there may be
    a more recent set of user journeys to develop the tests for.
"""

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase, override_settings, tag
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from project_apps.aimodels.tests.tests_models import create_ai_model
from standard.tests.selenium import SeleniumMixin

""" SECTION 1 """
from project_apps.chats.models import ConversationItem, ConversationThread
from project_apps.chats.tests.tests_models import (
    create_conversation_item,
    create_conversation_items,
    create_conversation_thread,
)

""" SECTION 3 """
# Checks lists for the basics on each page
CHECK_CONVERSATIONTHREAD_LIST = [
    "AIUI Chat",
    "Models",
    "Start a new",
    "Browse",
    "Conversation Threads",
]
CHECK_CONVERSATIONTHREAD_DETAIL = [
    "Details for ConversationThread:",
    "ConversationThread ConversationItems",
    "Edit ConversationThread",
    "Delete ConversationThread",
    "Procedure ConversationThread",
    "Back to ConversationThread",
]
CHECK_CONVERSATIONTHREAD_CREATE = [
    "New Chat",
    "Conversation Name",
    "Conversation AI Models",
    "Start chat",
]
CHECK_CONVERSATIONTHREAD_EDIT = [
    "Edit ConversationThread",
    "ConversationThread ConversationItems",
    "ConversationThread field1",
    "ConversationThread field2",
    "ConversationThread field3",
    "ORDER",
]
CHECK_CONVERSATIONTHREAD_DELETE = [
    "Delete ConversationThread",
    "ConversationThread ConversationItems",
    "Delete",
]


class ConversationThreadManagementTest(SeleniumMixin, LiveServerTestCase):
    """
    The base class for tests about a user performing ConversationThread management actions

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
        _test_click_add_conversationitem_form_fails
        _go_to_conversationthread_list
        _check_in_page
        _check_not_in_page
        _add_conversationitem
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

    def setUp(self):
        super().setUp()
        self.ai_model = create_ai_model(
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

    def _test_click_add_conversationitem_form_fails(self):
        with self.assertRaises(
            ElementClickInterceptedException,
            msg="Allowing addition of form when shouldn't be",
        ):
            self.selenium.find_element_by_id("add-ConversationItem-form").click()

    def _go_to_conversationthread_list(self):
        self.go_home()
        self.selenium.implicitly_wait(5)
        # and is now at the home page
        self.assertIn("Home - AIUI", self.selenium.title)
        self.assertIn(
            "Models",
            self.selenium.page_source,
        )

        # Then open the side bar
        self._open_side_bar()
        # They then click on the Model link to go to the list page.
        # self._scroll_to_element_id_and_click("aimodels")

    def _add_conversationitem(self, num_items, start_range=0, add_to_item_number=0):
        for item_number in range(start_range, start_range + num_items):
            self._data_entry(
                f"id_ConversationItem-{item_number}-text",
                f"ConversationItem {item_number+add_to_item_number}",
            )
            self._data_entry(f"id_ConversationItem-{item_number}-when", "9am")
            item_order_box = self.selenium.find_element_by_id(
                f"id_ConversationItem-{item_number}-ORDER"
            )
            self.assertEqual(
                item_order_box.get_attribute("value"), str(item_number + 1)
            )
            self._scroll_to_element_id_and_click("add-ConversationItem-form")

    def _check_elements_values(self, elements_to_be_checked):
        for element, value in elements_to_be_checked.items():
            item_input = self.selenium.find_element_by_id(element)
            self.assertEqual(item_input.get_attribute("value"), value)


@tag("selenium")
@override_settings(ALLOWED_HOSTS=["*"])
@override_settings(SECURE_SSL_REDIRECT=False)
@override_settings(CSRF_COOKIE_SECURE=False)
@override_settings(SESSION_COOKIE_SECURE=False)
class ConversationThreadManagementTestLists(ConversationThreadManagementTest):
    """
    This class makes tests about a user looking at lists of ConversationThreads

    Attributes:

    methods:
        SeleniumMixin
            user_login
            _set_up_web_driver
            _tear_down_web_driver
            _data_entry
            _scroll_to_element_id_and_click
        ConversationThreadManagementTest
            setUpClass
            tearDownClass
            setUp
            _test_click_add_conversationitem_form_fails
            _go_to_conversationthread_list
            _check_in_page
            _check_not_in_page
            _add_conversationitem
            _check_elements_values
        test_view_lists
        test_view_lists_empty
        test_view_lists_not_logged_in
    """

    def test_view_lists(self):
        """
        This function tests the ability of an existing user to view any existing lists
        of ConversationThread.

        preconditions:
            A user with an account.
            Two conversationthreads already existing to form a list

        results:
            User can see a list of conversationthreads that are available.
        """
        conversation_thread = create_conversation_thread(
            self.senior_user, "Thread 1", "Summary for the thread", "web", self.ai_model
        )
        create_conversation_thread(
            self.senior_user, "Thread 2", "Summary for the thread", "web", self.ai_model
        )
        self._go_to_conversationthread_list()

        # Now on the list page the user can see the requisite list of ConversationThreads
        self._check_in_page(CHECK_CONVERSATIONTHREAD_LIST)
        # displaying currently available lists
        self._check_in_page(
            [
                "Thread 1",
                "Thread 2",
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
        self.go_home()

        # Now on the list page the user can see there are no ConversationThreads
        self._check_in_page(
            [
                "Start Your First Chat",
                "Get AIUI working",
                "Start a chat",
            ]
        )
        # Now open the side bar
        self._open_side_bar()

        # and check there are no conversation threads.
        self._check_in_page(["No chats yet."])
        self._check_not_in_page(["Thread 1", "Thread 2"])


@tag("selenium")
@override_settings(ALLOWED_HOSTS=["*"])
@override_settings(SECURE_SSL_REDIRECT=False)
@override_settings(CSRF_COOKIE_SECURE=False)
@override_settings(SESSION_COOKIE_SECURE=False)
class ConversationThreadManagementTestDetail(ConversationThreadManagementTest):
    """
    This class makes tests about a user viewing the details of an instance of
    ConversationThread.

    Attributes:

    methods:
        SeleniumMixin
            user_login
            _set_up_web_driver
            _tear_down_web_driver
            _data_entry
            _scroll_to_element_id_and_click
        ConversationThreadManagementTest
            setUpClass
            tearDownClass
            setUp
            _test_click_add_conversationitem_form_fails
            _go_to_conversationthread_list
            _check_in_page
            _check_not_in_page
            _add_conversationitem
            _check_elements_values
        test_view_conversationthread_detail
        test_view_conversationthread_detail_not_logged_in
    """


''' SECTION 6
    def test_conversationthread_view_detail(self):
        """
        This function tests an existing user viewing the details of an instance
        of ConversationThread.

        preconditions:
            A user with an account.
            a list in the db

        results:
            User can see a the details of the list.
        """
        # Two lists already exist
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitems(self.user, first_conversationthread)
        create_conversationthread(self.user, field1, field2, field3)

        self._go_to_conversationthread_list()

        # This takes them to the list page displaying currently available lists
        # So they click on the first one to see it's details.
        self.selenium.find_element_by_link_text(first_conversationthread.field1).click()
        self.assertIn("PROJECT NAME - APP NAME Details", self.selenium.title)
        self._check_in_page(CHECK_CONVERSATIONTHREAD_DETAIL)

        # ...and are able to see various details for that list.
        self._check_in_page(
            [
                first_conversationthread.field1,
                first_conversationthread.field2,
                first_conversationthread.field3,
                "The first conversationitem",
                "The fifth conversationitem",
            ]
        )

    def test_view_conversationthread_detail_not_logged_in(self):
        """
        This function tests that viewing the detail of a conversationthread
        requires a user to be logged in

        preconditions:
            Trying to access conversationthread detail page but not logged in
            A list in the DB

        results:
            Tring to view the procedures detail without being logged in will require a login.
        """
        # A conversationthread already exist
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)

        self.selenium.get(f"{self.live_server_url}/conversationthread/{first_conversationthread.id}/")
        self.assertIn(
            "Honeybyte Intranet Login",
            self.selenium.page_source,
        )
        self.user_login("senior@project.com", "testpass123")
        self.selenium.implicitly_wait(5)
        self.assertIn("PROJECT NAME - APP NAME Details", self.selenium.title)
'''


@tag("selenium")
@override_settings(ALLOWED_HOSTS=["*"])
@override_settings(SECURE_SSL_REDIRECT=False)
@override_settings(CSRF_COOKIE_SECURE=False)
@override_settings(SESSION_COOKIE_SECURE=False)
class ConversationThreadManagementTestCreate(ConversationThreadManagementTest):
    """
    This class makes tests about a user performing ConversationThread creation actions

    Attributes:

    methods:
        SeleniumMixin
            user_login
            _set_up_web_driver
            _tear_down_web_driver
            _data_entry
            _scroll_to_element_id_and_click
        ConversationThreadManagementTest
            setUpClass
            tearDownClass
            setUp
            _test_click_add_conversationitem_form_fails
            _go_to_conversationthread_list
            _check_in_page
            _check_not_in_page
            _add_conversationitem
            _check_elements_values
        _go_to_create
        _add_base_fields
        test_view_conversationthread_create
        test_view_conversationthread_create_DISALLOW_multiple_add_conversationitem_form_clicks
        test_view_conversationthread_create_add_conversationitem_form_ordering
        test_view_conversationthread_create_conversationitem_changing_order
        test_view_conversationthread_create_delete_extra_conversationitem_form_from_conversationthread
        test_view_conversationthread_create_delete_extra_conversationitem_form_with_fieldvalue_entered_from_conversationthread
        test_view_conversationthread_create_no_requiredfield
        test_view_conversationthread_create_no_duplicate_fieldnottobeduplicated
        test_view_conversationthread_create_no_duplicate_conversationitem_fieldnottobeduplicated_for_same_conversationthread
        test_view_conversationthread_create_CAN_duplicate_conversationitem_fieldnottobeduplicated_for_different_conversationthread
        test_view_conversationthread_create_not_logged_in
    """

    def _go_to_create(self):
        # User clicks on the create link to add a new list.
        self.go_home()
        self._open_side_bar()

    def _add_base_fields(self):
        self._data_entry("id_name", "A brand new chat")
        select_ai_model_element = self.selenium.find_element(By.ID, "id_aimodel")
        select_ai_model = Select(select_ai_model_element)
        select_ai_model.select_by_visible_text("4o")

    def test_view_conversation_thread_create_no_existing(self):
        """
        This function tests an existing user creating a conversationthread
        with conversationitem.

        preconditions:
            A user with an account.

        results:
            User can see the list detail page with the details for the list they just
            created.
        """
        # Now the user logins into the app and opens the side bar on the home page
        self._go_to_create()
        # ...and click on start new chat.
        self._scroll_to_element_id_and_click("start-new-chat")
        self._check_in_page(CHECK_CONVERSATIONTHREAD_CREATE)
        # Now they add the base fields for a ConversationThread.
        self._add_base_fields()
        # Clicks save
        self._scroll_to_element_id_and_click("id-save-chat")
        self.selenium.implicitly_wait(5)
        # and can see they are in the detail page
        self.assertIn("Home - AIUI", self.selenium.title)
        self._scroll_to_element_id_and_click("chat-model-details")
        # ...and are able to see various details for that list.
        # and they are the same as the ones inputed in creation
        conversation_threads = ConversationThread.objects.all()
        self.assertEqual(conversation_threads.count(), 1)
        self._check_in_page(
            [
                "General-purpose coding and writing",
                "Fast completions and visual input understanding",
                "A brand new chat",
            ]
        )

    # TODO: There seems to be issues with the test below being included due to race conditions on the database.
    # def test_view_conversation_thread_create_one_existing(self):
    #     """
    #     This function tests an existing user creating a conversationthread
    #     with conversationitem.

    #     preconditions:
    #         A user with an account.

    #     results:
    #         User can see the list detail page with the details for the list they just
    #         created.
    #     """
    #     # A conversationthread already exists.
    #     create_conversation_thread(
    #         self.senior_user, "Test Thread", "Test Summary", "web", self.ai_model
    #     )
    #     # Now the user logins into the app and opens the side bar on the home page
    #     self._go_to_create()
    #     # ...and click on start new chat.
    #     self._scroll_to_element_id_and_click("start-new-chat")
    #     self._check_in_page(CHECK_CONVERSATIONTHREAD_CREATE)
    #     # Now they add the base fields for a ConversationThread.
    #     self._add_base_fields()
    #     # Clicks save
    #     self._scroll_to_element_id_and_click("id-save-chat")
    #     self.selenium.implicitly_wait(5)
    #     # and can see they are in the detail page
    #     self.assertIn("Home - AIUI", self.selenium.title)
    #     self._scroll_to_element_id_and_click("chat-model-details")
    #     # ...and are able to see various details for that list.
    #     # and they are the same as the ones inputed in creation
    #     conversation_threads = ConversationThread.objects.all()
    #     self.assertEqual(conversation_threads.count(), 2)
    #     self._check_in_page(
    #         [
    #             "General-purpose coding and writing",
    #             "Fast completions and visual input understanding",
    #             "Test Thread",
    #             "A brand new chat",
    #         ]
    #     )


@tag("selenium")
@override_settings(ALLOWED_HOSTS=["*"])
@override_settings(SECURE_SSL_REDIRECT=False)
@override_settings(CSRF_COOKIE_SECURE=False)
@override_settings(SESSION_COOKIE_SECURE=False)
class ConversationThreadManagementTestUpdate(ConversationThreadManagementTest):
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
        ConversationThreadManagementTest
            setUpClass
            tearDownClass
            setUp
            _test_click_add_conversationitem_form_fails
            _go_to_conversationthread_list
            _check_in_page
            _check_not_in_page
            _add_conversationitem
            _check_elements_values
        test_view_conversationthread_update_conversationthread_basefields
        test_view_conversationthread_update_no_requiredfield
        test_view_conversationthread_update_no_duplicate_fieldnottobeduplicated
        test_view_conversationthread_update_NO_duplicate_conversationitem_fieldnottobeduplicated_for_same_conversationthread
        test_view_conversationthread_update_add_new_conversationitem_to_conversationthread
        test_view_conversationthread_update_DISALLOW_multiple_add_conversationitem_form_clicks
        test_view_conversationthread_update_add_conversationitem_form_ordering
        test_view_conversationthread_update_add_new_conversationitem_to_conversationthread_changing_order
        test_view_conversationthread_update_delete_existing_conversationitem_from_conversationthread
        test_view_conversationthread_update_delete_extra_conversationitem_form_from_conversationthread
        test_view_conversationthread_update_delete_extra_conversationitem_form_with_text_entered_from_conversationthread
        test_view_conversationthread_update_CAN_duplicate_conversationitem_fieldnottobeduplicated_for_different_conversationthread
        test_view_conversationthread_update_not_logged_in
    """


''' SECTION 8
    def _go_to_edit(self, conversationthread):
        self.selenium.find_element_by_link_text(conversationthread.field1).click()
        self.assertIn("PROJECT NAME - APP NAME Details", self.selenium.title)

        self._scroll_to_element_id_and_click("edit-conversationthread")
        self.assertIn("PROJECT NAME - APP NAME Update", self.selenium.title)

    def test_view_conversationthread_update_conversationthread_basefields(self):
        """
        This function tests an existing user updating the basefields of a conversationthread
        without conversationitem.

        preconditions:
            A user with an account.
            a conversationthread already saved to the database.

        results:
            User can see the conversationthread detail page with the details for the conversationthread they just
            updated.
        """
        # A conversationthread already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)

        self._go_to_conversationthread_list()
        # This takes them to the conversationthread list page
        # displaying currently available conversationthreads

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(first_conversationthread)

        # .. and can see they are in the edit page
        self._check_in_page(CHECK_CONVERSATIONTHREAD_EDIT)

        # ...and are able to see various details of the list ready for changing.
        self._check_in_page(
            [
                "field1 value",
                "field2 value",
                "field3 value",
            ]
        )

        # Now they add the name and description for the List
        self._data_entry("id_field1", "field1 value changed")
        self._data_entry("id_field2", "field2 value changed")

        # Clicks update
        self._scroll_to_element_id_and_click("id-update-conversationthread")

        # and can see the item that they created
        self.assertIn("PROJECT NAME - APP NAME Details", self.selenium.title)

        # ...and are able to see various details for that list.
        # and they are the same as the ones inputted at update
        self._check_in_page(
            [
                "field1 value changed",
                "field2 value changed",
                "field3 value",
            ]
        )

    def test_view_conversationthread_update_no_requiredfield(self):
        """
        This function tests an existing user trying to update a conversationthread without a requiredfield.

        preconditions:
            An existing conversationthread
            A user with an account.

        results:
            User can see the conversationthread update page with the details for the conversationthread they just
            updated and an error message - "Please fill out this field."
        """
        # A conversationthread already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)

        self._go_to_conversationthread_list()
        # This takes them to the conversationthread list page
        # displaying currently available conversationthreads

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(first_conversationthread)

        # Now they delete the name and change the description for the List
        self._data_entry("id_requiredfield", "")
        self._data_entry("id_field2", "field2 value")

        # Clicks update
        self._scroll_to_element_id_and_click("id-update-conversationthread")

        # but sees that they are still on the list update page
        self.assertIn("PROJECT NAME - APP NAME Update", self.selenium.title)

        validation_message = (
            WebDriverWait(self.selenium, 20)
            .until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input#id_requiredfield[name='requiredfield']"))
            )
            .get_attribute("validationMessage")
        )
        # with an error message
        self.assertIn("Please fill out this field.", validation_message)

    def test_view_conversationthread_update_no_duplicate_fieldnottobeduplicated(self):
        """
        This function tests an existing user trying to update a conversationthread with a fieldnottobeduplicated
        that already exists for an existing conversationthread

        preconditions:
            A user with an account.
            Two existing conversationthreads

        results:
            User can see the conversationthread update page with the details for the conversationthread they just
            updated and an error message - "The fieldnottobeduplicated for this conversationthread already exists"
        """
        # Given two conversationthreads already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        second_conversationthread = create_conversationthread(self.user, field1, field2, field3)

        self._go_to_conversationthread_list()
        # This takes them to the conversationthread list page
        # displaying currently available conversationthreads

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(second_conversationthread)

        # ...and are able to see various details of the list ready for changing.
        self._check_in_page(
            [
                "field1 value",
                "field2 value",
                "field3 value",
            ]
        )

        # Now they change the name for the List to one that already exists
        self._data_entry("id_fieldnottobeduplicated", "Duplicate value")

        # Clicks update
        self._scroll_to_element_id_and_click("id-update-conversationthread")

        # but sees that they are still on the list update page
        self.assertIn("PROJECT NAME - APP NAME Update", self.selenium.title)

        # ...with the various details for that list.
        self._check_in_page(
            [
                "Duplicate value",
                "field2 value",
                # and an error message
                "The fieldnottobeduplicated for this conversationthread already exists",
            ]
        )

    def test_view_conversationthread_update_NO_duplicate_conversationitem_fieldnottobeduplicated_for_same_conversationthread(self):
        """
        This function tests an existing user trying to update a conversationthread with two
        conversationitem with the same fieldnottobeduplicated

        preconditions:
            A conversationthread with conversationitems
            A user with an account.

        results:
            User can see the conversationthread update page with the details for the conversationthread they just
            updated and an error message - "conversationitem in a conversationthread must have distinct fieldnottobeduplicated"
        """
        # A conversationthread already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitem(self.user, first_conversationthread, fieldnottobeduplicated, itemfield2)
        create_conversationitem(self.user, first_conversationthread, itemfield1, itemfield2)

        self._go_to_conversationthread_list()
        # This takes them to the conversationthread list page
        # displaying currently available conversationthreads

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(first_conversationthread)

        # They change the text for the second list item to the same as the first list item
        if (
            self.selenium.find_element_by_id("id_conversationitem-0-fieldnottobeduplicated").get_attribute("value")
            == "Duplicate Value"
        ):
            self._data_entry("id_conversationitem-1-fieldnottobeduplicated", "Duplicate value")
        else:
            self._data_entry("id_conversationitem-0-fieldnottobeduplicated", "Duplicate value")

        # Clicks update
        self._scroll_to_element_id_and_click("id-update-conversationthread")

        # but sees that they are still on the list update page
        self.assertIn("PROJECT NAME - APP NAME Update", self.selenium.title)

        # ...with the various details for that list.
        self._check_in_page(
            [
                "Duplicate value",
                "field2 value",
                # and an error message
                "conversationitem in a conversationthread must have distinct fieldnottobeduplicated",
            ]
        )

    def test_view_conversationthread_update_add_new_conversationitem_to_conversationthread(self):
        """
        This function tests an existing user trying to update a conversationthread with
        new conversationitems

        preconditions:
            A conversationthread with conversationthread items
            A user with an account.

        results:
            User can see the conversationthread details page with the details for the conversationthread they just
            updated
        """
        # A conversationthread already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitem(self.user, first_conversationthread, fieldnottobeduplicated, itemfield2)
        create_conversationitem(self.user, first_conversationthread, itemfield1, itemfield2)

        self._go_to_conversationthread_list()
        # This takes them to the conversationthread list page
        # displaying currently available conversationthreads

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(first_conversationthread)

        # now add two new conversationitems and enter new data
        self._data_entry("id_conversationitem-2-itemfield1", "itemfield1 value")
        self._data_entry("id_conversationitem-2-itemfield2", "itemfield2 value")
        self._scroll_to_element_id_and_click("add-conversationitem-form")
        self._data_entry("id_conversationitem-3-itemfield1", "itemfield1 value")
        self._data_entry("id_conversationitem-3-itemfield2", "itemfield2 value")

        # Clicks update
        self._scroll_to_element_id_and_click("id-update-conversationthread")

        # and can see the item that they created
        self.assertIn("PROJECT NAME - APP NAME Details", self.selenium.title)

        # ...with the various details for the edited list.
        self._check_in_page(
            [
                "field1 value",
                "field2 value",
                "field3 value",
                "The first conversationitem",
                "The second conversationitem",
                # and the new conversationitems
                "3. itemfield1 value",
                "4. itemfield1 value",
            ]
        )

    def test_view_conversationthread_update_DISALLOW_multiple_add_conversationitem_form_clicks(self):
        """
        This function tests an existing user updating a conversationthread with conversationitems
        and clicking the add conversationitem form a number of times.

        preconditions:
            A user with an account.
            An existing conversationthread

        results:
            User can see the conversationthread detail page with the details for the conversationthread they just
            created with correct number ordering
        """
        # A conversationthread already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitem(self.user, first_conversationthread, fieldnottobeduplicated, itemfield2)
        create_conversationitem(self.user, first_conversationthread, itemfield1, itemfield2)

        self._go_to_conversationthread_list()
        # This takes them to the conversationthread list page
        # displaying currently available conversationthreads

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(first_conversationthread)

        # Now adds an item but trying to click Add Another List Item at
        # wrong point in work flow
        self._test_click_add_conversationitem_form_fails()
        self._add_conversationitem(2, start_range=2, add_to_item_number=1)

        item_order_box = self.selenium.find_element_by_id("id_conversationitem-2-ORDER")
        self.assertEqual(item_order_box.get_attribute("value"), "3")
        item_order_box = self.selenium.find_element_by_id("id_conversationitem-3-ORDER")
        self.assertEqual(item_order_box.get_attribute("value"), "4")

        # with one last attempt at multiple Add Another conversationitem clicks
        self._scroll_to_element_id_and_click("add-conversationitem-form")
        self._test_click_add_conversationitem_form_fails()

        # Clicks update
        self._scroll_to_element_id_and_click("id-update-conversationthread")

        # and can see the item that they created
        self.assertIn("PROJECT NAME - APP NAME Details", self.selenium.title)

        # ...and are able to see various details for that list
        self._check_in_page(
            [
                "The first conversationitem",
                "The fourth conversationitem",
            ]
        )

    def test_view_conversationthread_update_add_conversationitem_form_ordering(self):
        """
        This function tests an existing user editing a conversationthread with conversationitems
        and messing around with conversationitems affecting ordering.

        preconditions:
            A user with an account.
            An exisitng conversationthread

        results:
            User can see the conversationthread detail page with the details for the conversationthread they just
            updated with correct number ordering
        """
        # A conversationthread already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitem(self.user, first_conversationthread, fieldnottobeduplicated, itemfield2)
        create_conversationitem(self.user, first_conversationthread, itemfield1, itemfield2)

        self._go_to_conversationthread_list()
        # This takes them to the conversationthread list page
        # displaying currently available conversationthreads

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(first_conversationthread)

        # then they add a couple of items
        self._add_conversationitem(2, start_range=2, add_to_item_number=1)
        self._check_elements_values(
            {
                "id_conversationitem-2-itemfield1": "itemfield1 3",
                "id_conversationitem-2-ORDER": "3",
                "id_conversationitem-3-itemfield1": "itemfield1 4",
                "id_conversationitem-3-ORDER": "4",
            }
        )

        # Now they decide that the second item shouldn't be there
        self._scroll_to_element_id_and_click("id_conversationitem-1-mark-deleted")

        # but that there should be another
        self._data_entry("id_conversationitem-4-itemfield1", "itemfield1 value 5")
        self._data_entry("id_conversationitem-4-itemfield2", "itemfield2 value")
        self._check_elements_values(
            {
                "id_conversationitem-0-ORDER": "1",
                "id_conversationitem-0-itemfield1": "itemfield1 0",
                "id_conversationitem-2-ORDER": "2",
                "id_conversationitem-2-itemfield1": "itemfield1 3",
                "id_conversationitem-3-ORDER": "3",
                "id_conversationitem-3-itemfield1": "itemfield1 4",
            }
        )

        # Now they decide that the first item shouldn't be there
        self._scroll_to_element_id_and_click("id_lconversationitem-0-mark-deleted")

        # but that there should be another
        self._scroll_to_element_id_and_click("add-conversationitem-form")
        self._data_entry("id_conversationitem-5-itemfield1", "itemfield1 value 6")
        self._data_entry("id_conversationitem-5-itemfield2", "itemfield2 value")

        self._check_elements_values(
            {
                "id_conversationitem-2-ORDER": "1",
                "id_conversationitem-2-itemfield1": "itemfield1 value 3",
                "id_conversationitem-3-ORDER": "2",
                "id_conversationitem-3-itemfield1": "itemfield1 value 4",
                "id_conversationitem-4-ORDER": "3",
                "id_conversationitem-4-itemfield1": "itemfield1 value 5",
            }
        )

    def test_view_conversationthread_update_add_new_conversationitem_to_conversationthread_changing_order(self):
        """
        This function tests an existing user trying to update a conversationthread with
        new conversationitems and the order of the conversationitems being changed.

        preconditions:
            A conversationthread with conversationitems
            A user with an account.

        results:
            User can see the conversationthread details page with the details for the conversationthread they just
            updated.
        """
        # A conversationthread already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitem(self.user, first_conversationthread, fieldnottobeduplicated, itemfield2)
        create_conversationitem(self.user, first_conversationthread, itemfield1, itemfield2)

        self._go_to_conversationthread_list()
        # This takes them to the conversationthread list page
        # displaying currently available conversationthreads

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(first_conversationthread)

        # now add two new conversationitems and enter new data
        self._data_entry("id_conversationitem-2-itemfield1", "itemfield1 value")
        self._data_entry("id_conversationitem-2-itemfield2", "itemfield2 value")
        self._scroll_to_element_id_and_click("add-conversationitem-form")
        self._data_entry("id_conversationitem-3-itemfield1", "itemfield1 value")
        self._data_entry("id_conversationitem-3-itemfield2", "itemfield2 value")


        # then decides the first one added is not required so clears the text
        self._scroll_to_element_id_and_click("id_conversationitem-2-mark-deleted")

        # Clicks update
        self._scroll_to_element_id_and_click("id-update-conversationthread")

        # and can see the item that they created
        self.assertIn("PROJECT NAME - APP NAME Details", self.selenium.title)

        # ...and are able to see various details for that list
        self._check_in_page(
            [
                "X. The first conversationitem",
                "X. The fourth conversationitem",
            ]
        )

    def test_view_conversationthread_update_delete_existing_conversationitem_from_conversationthread(self):
        """
        This function tests an existing user removing an existing conversationitem
        from an existing conversationthread

        preconditions:
            A conversationthread with conversationitems
            A user with an account.

        results:
            User can see the conversationthread details page with the details for the conversationthread they just
            updated.
        """
        # A conversationthread already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitem(self.user, first_conversationthread, fieldnottobeduplicated, itemfield2)
        create_conversationitem(self.user, first_conversationthread, itemfield1, itemfield2)

        self._go_to_conversationthread_list()
        # This takes them to the conversationthread list page
        # displaying currently available conversationthreads

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(first_conversationthread)

        # now click the DELETE checkbox for the second item
        self._scroll_to_element_id_and_click("id_conversationitem-1-DELETE")

        # Clicks update
        self._scroll_to_element_id_and_click("id-update-conversationthread")

        # and can see the item that they created
        self.assertIn("PROJECT NAME - APP NAME Details", self.selenium.title)

        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 1)

        saved_conversationitems = saved_conversationthreads[0].conversationitems.all()
        self.assertEqual(saved_conversationitems.count(), 1)

    def test_view_conversationthread_update_delete_extra_conversationitem_form_from_conversationthread(self):
        """
        This function tests an existing user removing an empty extra conversationitem
        formset form from an existing conversationthread

        preconditions:
            A conversationthread with conversationitems
            A user with an account.

        results:
            User can see the conversationthread details page with the details for the conversationthread they just
            updated.
        """
        # A conversationthread already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitem(self.user, first_conversationthread, fieldnottobeduplicated, itemfield2)
        create_conversationitem(self.user, first_conversationthread, itemfield1, itemfield2)

        self._go_to_conversationthread_list()
        # This takes them to the conversationthread list page
        # displaying currently available conversationthreads

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(first_conversationthread)

        # now click the DELETE checkbox for the second item
        self._scroll_to_element_id_and_click("id_conversationitem-2-DELETE")

        # Clicks update
        self._scroll_to_element_id_and_click("id-update-conversationthread")

        # and can see the item that they created
        self.assertIn("PROJECT NAME - APP NAME Details", self.selenium.title)

        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 1)

        saved_conversationitems = saved_conversationthreads[0].conversationitems.all()
        self.assertEqual(saved_conversationitems.count(), 2)

    def test_view_conversationthread_update_delete_extra_conversationitem_form_with_data_entered_from_conversationthread(self):
        """
        This function tests an existing user removing an empty extra conversationitem
        formset formthat has had data entered from an existing conversationthread

        preconditions:
            A conversationthread with conversationitems
            A user with an account.

        results:
            User can see the conversationthread details page with the details for the conversationthread they just
            updated.
        """
        # A conversationthread already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitem(self.user, first_conversationthread, fieldnottobeduplicated, itemfield2)
        create_conversationitem(self.user, first_conversationthread, itemfield1, itemfield2)

        self._go_to_conversationthread_list()
        # This takes them to the conversationthread list page
        # displaying currently available conversationthreads

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(first_conversationthread)

        # They now add some data to the extra form
        self._data_entry("id_conversationitem-2-itemfield1", "itemfield1 value")
        self._data_entry("id_conversationitem-2-itemfield2", "itemfield2 value")
        # now decide the extra item shouldn't be part of this list
        # now click the DELETE checkbox for the third item
        self._scroll_to_element_id_and_click("id_conversationitem-2-DELETE")

        # Clicks update
        self._scroll_to_element_id_and_click("id-update-conversationthread")

        # and can see the item that they created
        self.assertIn("PROJECT NAME - APP NAME Details", self.selenium.title)

        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 1)

        saved_conversationitems = saved_conversationthreads[0].conversationitems.all()
        self.assertEqual(saved_conversationitems.count(), 2)

    def test_view_conversationthread_update_CAN_duplicate_conversationitem_fieldnottobeduplicated_for_different_conversationthread(self):
        """
        This function tests an existing user trying to update a conversationthread with a conversationitem fieldnottobeduplicated
        that already exists on another conversationthread

        preconditions:
            A user with an account.
            Two existing conversationthreads with conversationitems

        results:
            User can see the conversationthread detail page with the details for the conversationthread they just
            updated with no error message.
        """
        # Two conversationthreads already exist
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitem(self.user, first_conversationthread, fieldnottobeduplicated, itemfield2)
        create_conversationitem(self.user, first_conversationthread, itemfield1, itemfield2)

        second_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitem(self.user, second_conversationthread, fieldnottobeduplicated, itemfield2)
        create_conversationitem(self.user, second_conversationthread, itemfield1, itemfield2)

        self._go_to_conversationthread_list()
        # This takes them to the conversationthread list page
        # displaying currently available conversationthreads

        # So they click on the first one to see it's details.
        # They see that there is an error in the list so click edit to make changes
        self._go_to_edit(first_conversationthread)

        # enter the new list item text that happens to be the same as a list item in
        # another list
        self._data_entry("id_conversationitem-0-fieldnottobeduplicated", "Duplicate value")

        # Clicks update
        self._scroll_to_element_id_and_click("id-update-conversationthread")

        # and can see the item that they created
        self.assertIn("PROJECT NAME - APP NAME Details", self.selenium.title)

        # displaying the changes for the list
        self._check_in_page(
            [
                "field1 value",
                "Duplicate value",
            ]
        )

    def test_view_conversationthread_update_not_logged_in(self):
        """
        This function tests that the update conversationthread view requires a user to be logged in

        preconditions:
            Trying to access /conversationthread/update but not logged in

        results:
            Trying to view the conversationthread update without being logged in will require a login.
        """
        # A conversationthread already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitem(self.user, first_conversationthread, fieldnottobeduplicated, itemfield2)
        create_conversationitem(self.user, first_conversationthread, itemfield1, itemfield2)

        self.selenium.get(f"{self.live_server_url}/conversationthread/update/{first_conversationthread.id}/")
        self.assertIn(
            "PROJECT NAME Login",
            self.selenium.page_source,
        )
        self.user_login("senior@project.com", "testpass123")
        self.selenium.implicitly_wait(5)
        self.assertIn("PROJECT NAME - APP NAME Update", self.selenium.title)
        self.assertIn(
            "field1 value",
            self.selenium.page_source,
        )
'''


@tag("selenium")
@override_settings(ALLOWED_HOSTS=["*"])
@override_settings(SECURE_SSL_REDIRECT=False)
@override_settings(CSRF_COOKIE_SECURE=False)
@override_settings(SESSION_COOKIE_SECURE=False)
class ConversationThreadManagementTestDelete(ConversationThreadManagementTest):
    """
    This class makes tests about a user performing ConversationThread delete actions

    Attributes:

    methods:
        SeleniumMixin
            user_login
            _set_up_web_driver
            _tear_down_web_driver
            _data_entry
            _scroll_to_element_id_and_click
        ConversationThreadManagementTest
            setUpClass
            tearDownClass
            setUp
            _test_click_add_conversationitem_form_fails
            _go_conversationthread_list
            _check_in_page
            _check_not_in_page
            _add_conversationitem
            _check_elements_values
        test_view_conversationthread_delete_not_logged_in
        test_view_conversationthread_delete_conversationthread
    """


''' SECTION 9
    def test_view_conversationthread_delete_not_logged_in(self):
        """
        This function tests that the delete conversationthread view requires a user to be logged in

        preconditions:
            conversationthreads already exist
            Trying to access /conversationthread/delete but not logged in

        results:
            Trying to view the conversationthread delete without being logged in will require a login.
        """
        # A conversationthread already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitem(self.user, first_conversationthread, fieldnottobeduplicated, itemfield2)
        create_conversationitem(self.user, first_conversationthread, itemfield1, itemfield2)


        self.selenium.get(f"{self.live_server_url}/conversationthreads/delete/{first_conversationthread.id}/")
        self.assertIn(
            "PROJECT NAME Login",
            self.selenium.page_source,
        )
        self.user_login("senior@project.com", "testpass123")
        self.selenium.implicitly_wait(5)
        self.assertIn("PROJECT NAME - APP NAME Delete", self.selenium.title)
        self.assertIn(
            "field1",
            self.selenium.page_source,
        )

    def test_view_conversationthread_delete_conversationthread(self):
        """
        This function tests an existing user deleting a conversationthread

        preconditions:
            A user with an account.
            a conversationthread already saved to the database.

        results:
            User can see the conversationthread procedures page without the details for the conversationthread they just
            deleted.
        """
        # A conversationthread already exists.
        first_conversationthread = create_conversationthread(self.user, field1, field2, field3)
        create_conversationitem(self.user, first_conversationthread, fieldnottobeduplicated, itemfield2)
        create_conversationitem(self.user, first_conversationthread, itemfield1, itemfield2)

        self._go_to_conversationthread_list()
        # This takes them to the conversationthread list page
        # displaying currently available conversationthreads

        # So they click on the first one to see it's details.
        self.selenium.find_element_by_link_text(first_conversationthread.name).click()
        self.assertIn("PROJECT NAME - APP NAME Details", self.selenium.title)

        # They see that there is a list that needs deleting so click delete
        self._scroll_to_element_id_and_click("delete-conversationthread")
        self.assertIn("PROJECT NAME - APP NAME Delete", self.selenium.title)
        self._check_in_page(CHECK_CONVERSATIONTHREAD_DELETE)

        # ...and are able to see various details of the list ready for deleting.
        self._check_in_page(
            [
                "field1 value",
                "field2 value",
            ]
        )

        # Clicks delete
        self._scroll_to_element_id_and_click("id-delete-conversationthread")

        # This takes them to the list page
        self.assertIn("PROJECT NAME - APP NAME", self.selenium.title)
        # displaying currently available conversationthread
        self.assertIn(
            "There are no conversationthread",
            self.selenium.page_source,
        )
'''
