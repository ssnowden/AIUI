""" This module unit defines mixins for base tests on models.

It has the test cases:
    ModelTestMixin: Simple setUp with a user created.
    ModelValidationTestMixin: Based on ModelTestMixin has basic validation tests enforcing 
        some model best practice (e.g. get_absolute_url).
"""
from django.contrib.auth import get_user_model


class ModelTestMixin:
    """
    This mixin class creates basis for model tests

    properties:

    methods:
        setUp
        test_list_verbose_name_and_verbose_name_plural
        test_list_field_verbose_name
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="junior@project.com", username="junior", password="testpass123"
        )


class ModelValidationTestMixin(ModelTestMixin):
    """
    This mixin class creates basis for model validation tests

    properties:

    methods:
        test_model_verbose_name_and_verbose_name_plural
        test_model_field_verbose_name
        test_model_class_string_attribute_set
        test_model_get_absolute_url
    """

    def test_model_verbose_name_and_verbose_name_plural(self):
        """
        This function tests that the List model has verbose name and verbose name plural set.

        args:

        returns:
        """
        self.assertEqual(self.model_class._meta.verbose_name_raw, self.verbose_name_raw)
        self.assertEqual(self.model_class._meta.verbose_name_plural, self.verbose_name_plural)

    def test_model_field_verbose_name(self):
        """
        This function tests that the a model's fields have verbose name set.

        args:

        returns:
        """
        for field, verbose_name in self.field_verbose_names.items():
            self.assertEqual(
                self.model_class._meta.get_field(field).verbose_name.title(), verbose_name
            )

    def test_model_class_string_attribute_set(self):
        """
        This function tests that the List model has a __string__ set.

        args:

        returns:
        """
        self.assertEqual(str(self.model_instance), self.str_test)

    def test_model_get_absolute_url(self):
        """
        This function tests that the List model has a get_absolute_url set.

        args:

        returns:
        """
        self.assertEqual(self.model_instance.get_absolute_url(), self.absolute_url)
