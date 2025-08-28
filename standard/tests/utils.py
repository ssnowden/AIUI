from django.contrib.auth import get_user_model
from django.test import RequestFactory


class UserSetupMixin:
    def setUp(self):
        user_model = get_user_model()
        self.user1 = user_model.objects.create_user(
            email="junior@project.com",
            username="junior",
            password="testpass123",
            terms_and_conditions=True,
        )
        """
        user_profile = UserProfile.objects.create(
            user=self.user1, is_primary_contact=True
        )
        # Create a new company with user.company_name
        other_model1 = OtherModel.objects.create(
            name="Test Company", created_by=self.user1, modified_by=self.user1
        )
        # Add company to user_profile
        user_profile.othermodels.add(other_model1)
        """
        self.user1.save()

        self.user2 = user_model.objects.create_user(
            email="tempstaff@project.com",
            username="tempstaff",
            password="testpass123",
            terms_and_conditions=True,
        )
        """
        user_profile = UserProfile.objects.create(
            user=self.user2, is_primary_contact=True
        )
        # Create a new company with user.company_name
        new_other_model = OtherModel.objects.create(
            name="A Different Test Company", created_by=self.user2, modified_by=self.user2
        )
        # Add other model to user_profile
        user_profile.othermodels.add(new_company)
        user_profile.othermodels.add(other_model1)
        """
        self.user2.save()


def generate_request(
    request_type, url, user, data=None, query_string=None, header=None
):
    """
    This is a helper function that generates a http request for a given url with a
    given user.

    args:
        url: The url being requested
        user: the user making the request

    returns:
        request: the http request generated
    """
    header = header or {}
    request_methods = {
        "GET": RequestFactory().get,
        "POST": RequestFactory().post,
    }
    request = request_methods[request_type](
        url,
        data=data if request_type == "POST" else None,
        QUERY_STRING=query_string,
        **header,
    )

    request.user = user

    return request


def check_view_setup(test_case_instance, view_class, model, view_object_name, template):
    """
    This is a helper function that tests the basics of a view.

    args:
        test_case_instance: The TestCase that is running the instance (passes in self)
        view_class: the class of the view that will be tested
        model: the expected model for this view
        view_object_name: The expected name for the view's object
        template: The expected template the view will use to render a response

    returns:
        None
    """
    view = view_class()
    test_case_instance.assertEqual(view.model, model)
    test_case_instance.assertEqual(view.context_object_name, view_object_name)
    test_case_instance.assertEqual(view.template_name, template)


def test_view_setup(
    test_case_instance,
    view_class,
    model,
    form_class=None,
    view_object_name=None,
    template=None,
):
    """
    This is a helper function that tests the basics of a create view.

    args:
        test_case_instance: The TestCase that is running the instance (passes in self)
        view_class: the class of the view that will be tested
        model: the expected model for this view
        view_object_name: The expected name for the view's object
        template: The expected template the view will use to render a response

    returns:
        None
    """
    view = view_class()
    test_case_instance.assertEqual(view.model, model)
    if form_class is not None:
        test_case_instance.assertEqual(view.form_class, form_class)
    if view_object_name is not None:
        test_case_instance.assertEqual(view.context_object_name, view_object_name)
    if template is not None:
        test_case_instance.assertEqual(view.template_name, template)


def setup_view_request(view_class, request, object_for_test=None):
    """
    This is a helper function that sets a view up with a request.

    args:
        view_class: the class of the view that will be tested
        request: The request for the view
        object_for_test: OPTIONAL - for views expecting an identifier for an object

    returns:
        test_view: An instance of the view to be tested setup with a request
    """
    test_view = view_class()
    if object_for_test is None:
        test_view.setup(request)
    else:
        test_view.setup(request, pk=object_for_test)
    return test_view


def check_object(test_instance, object, attribute_tests):
    """
    This function attempts a number of assertions against a list

    args:

    returns:
    """
    for attribute_name, attribute_value in attribute_tests.items():
        attribute_for_test = getattr(object, attribute_name)
        if isinstance(attribute_value, bool):
            test_instance.assertEqual(attribute_for_test, attribute_value)
        else:
            test_instance.assertEqual(str(attribute_for_test), attribute_value)
