from django.contrib.auth import get_user_model


class FormTestMixin:
    """
    This mixin sets up tests for a basic Form.

    properties:

    methods:
        setUp
        _check_in
        _check_not_in
        test_form_html
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="junior@project.com", username="junior", password="testpass123"
        )

    def _check_in(self, form_html, in_list):
        for item in in_list:
            self.assertIn(item, form_html)

    def _check_not_in(self, form_html, not_in_list):
        for item in not_in_list:
            self.assertNotIn(item, form_html)

    def test_form_html(self):
        form = self.form_class()
        form_html = form.as_p()

        self.assertFalse(form.is_bound)
        self._check_not_in(form_html, self.not_in_html_list)
        self._check_in(form_html, self.in_html_list)


class FormWithForeignKeyTestMixin(FormTestMixin):
    """
    This mixin sets up tests for a Form that has a foriegn key.

    properties:

    methods:
        test_form_html
    """

    def test_form_html(self):
        form = self.form_class(instance=self.foreign_key_instance)

        form_html = form.as_p()

        self.assertFalse(form.is_bound)
        self._check_not_in(form_html, self.not_in_html_list)
        self._check_in(form_html, self.in_html_list)


class FormsetTestMixin(FormTestMixin):
    """
    This mixin sets up tests for a basic Formset.

    properties:

    methods:
        test_form_html
    """

    def test_form_html(self):
        formset = self.formset_class(
            queryset=self.formset_queryset,
            prefix=self.formset_prefix,
            instance=self.foreign_key_instance,
        )

        for index, form in enumerate(formset):
            form_html = form.as_p()

            self.assertFalse(form.is_bound)
            self._check_not_in(form_html, self.not_in_html_list)
            self.in_html_list.append(
                f'name="list_item-{index}-text" class="form-control form-control-md"'
            )
            self._check_in(form_html, self.in_html_list)
            del self.in_html_list[len(self.in_html_list) - 1]
