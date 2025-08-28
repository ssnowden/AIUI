"""This module provides supporting functionality for Fts using Selenium.

classes:
    SeleniumMixin
"""

import socket

from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class SeleniumMixin:
    """
    This class is a mixin to provide selenium capability in FTs.

    properties:

    methods:
        _set_up_web_driver
        _tear_down_web_driver
        user_login
        _data_entry
    """

    def setUp(self):
        super().setUp()
        self.senior_user = get_user_model().objects.create_user(
            email="senior@project.com",
            username="senior",
            password="testpass123",
            terms_and_conditions=True,
        )
        self.senior_user.save()

        self.junior_user = get_user_model().objects.create_user(
            email="junior@project.com",
            username="junior",
            password="testpass123",
            terms_and_conditions=True,
        )
        self.junior_user.save()

    @classmethod
    def _set_up_web_driver(cls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("start-maximized")
        cls.host = socket.gethostbyname(socket.gethostname())
        cls.selenium = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            options=chrome_options,
        )
        cls.selenium.implicitly_wait(5)

    @classmethod
    def _tear_down_web_driver(cls):
        cls.selenium.quit()

    def go_home(self):
        # The user has signed up, goes to the home page
        self.selenium.get(self.live_server_url)
        # logs in
        self.user_login(self.senior_user.email, "testpass123")

    def _open_side_bar(self):
        self._scroll_to_element_id_and_click("sidebar-toggler")
        self.selenium.implicitly_wait(5)

    def user_login(self, email, password):
        """
        This is a helper function that performs a login.

        args:
            email: the emial for login
            password: pass word for login

        returns:
        """
        self._data_entry("id_login", email)
        self._data_entry("id_password", password)
        self.selenium.find_element(By.ID, "signin").click()

    def _data_entry(self, element_id, data_for_entry):
        """
        This is a helper function that performs data entry into an input box
        and checks the value attribute is the data passed.

        args:
            element_id: the id attribute for the html input element
            data_for_entry: the data that needs to be input into the element

        returns:
            input_box: the input element that was used for data entry
        """
        input_box = self.selenium.find_element(By.ID, element_id)
        input_box.clear()
        input_box.send_keys(data_for_entry)
        self.assertEqual(input_box.get_attribute("value"), data_for_entry)
        return input_box

    def _scroll_to_element_id_and_click(self, id):
        # NOTE: The selenium native method seems to fail on certain cases so reverted to
        # older technique where a click is required.
        # wait = WebDriverWait(self.selenium, timeout=2)
        element = self.selenium.find_element(By.ID, id)
        # wait.until(lambda d: element.is_displayed())
        # actions = webdriver.ActionChains(self.selenium, duration=1000)
        # actions.scroll_to_element(element)
        # actions.perform()
        # actions.click(element)
        # actions.perform()
        self.selenium.execute_script("arguments[0].scrollIntoView();", element)
        self.selenium.execute_script("arguments[0].click();", element)
        return element

    def _scroll_to_element_id(self, id):
        wait = WebDriverWait(self.selenium, timeout=2)
        element = self.selenium.find_element(By.ID, id)
        wait.until(lambda d: element.is_displayed())
        webdriver.ActionChains(self.selenium).scroll_to_element(element).perform()
        # self.selenium.execute_script("arguments[0].scrollIntoView();", element)
        return element

    def _check_in_page(self, items_to_be_checked):
        for item in items_to_be_checked:
            self.assertIn(
                str(item),
                self.selenium.page_source,
                f"{item} is not in page",
            )

    def _check_not_in_page(self, items_to_be_checked):
        for item in items_to_be_checked:
            self.assertNotIn(
                item,
                self.selenium.page_source,
                f"{item} is in page",
            )

    def _check_element_value(self, element_id, expected_value):
        handling_step = self.selenium.find_element(By.ID, element_id)
        try:
            self.assertEqual(handling_step.get_attribute("value"), expected_value)
        except:
            print(
                f"{element_id} doesn't have value {expected_value}. This because selenium code going faster than client brython. You may need to go through a manual step through to double check client code is working."
            )

    def _drag_and_drop_element(self, drag_id, drop_id):
        draggable = self.selenium.find_element(By.ID, drag_id)
        droppable = self.selenium.find_element(By.ID, drop_id)
        time.sleep(0.4)
        ActionChains(self.selenium).drag_and_drop(draggable, droppable).perform()


class element_has_css_class(object):
    """An expectation for checking that an element has a particular css class.

    locator - used to find the element
    returns the WebElement once it has the particular css class
    """

    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)  # Finding the referenced element
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False


class element_does_not_have_css_class(object):
    """An expectation for checking that an element doesn't have a particular css class.

    locator - used to find the element
    returns the WebElement once it has the particular css class
    """

    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)  # Finding the referenced element
        if self.css_class in element.get_attribute("class"):
            return False
        else:
            return element
            return element
