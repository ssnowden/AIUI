"""This module unit tests the views for the chats app.

It has the test cases:
    CreateConversationThreadFormTest:
    CreateConversationItemFormTest:
    CreateConversationItemFormsetTest:
    UpdateConversationItemFormTest:
    UpdateConversationItemFormsetTest:
"""

from django.test import TestCase, tag

from project_apps.aimodels.tests.tests_models import create_ai_model
from project_apps.chats.forms import (
    ConversationItemForm,
    ConversationItemFormset,
    ConversationThreadForm,
)
from project_apps.chats.models import ConversationItem, ConversationThread
from project_apps.chats.tests.tests_models import (
    create_conversation_item,
    create_conversation_thread,
)
from standard.tests.utils import UserSetupMixin


@tag("form")
class CreateConversationThreadFormTest(UserSetupMixin, TestCase):
    """
    This class performs basic tests for the ConversationThread Create Form.

    Attributes:

    methods:
        setUp
        test_create_conversationthread_form_html
        test_create_conversationthread_form_validation_blank_fields
        test_create_conversationthread_form_validation_ok
        test_create_conversationthread_form_for_duplicate_conversationthread_fieldnottobeduplicated

    """

    def setUp(self):
        super().setUp()
        self.ai_model = create_ai_model(
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

    def test_create_conversationthread_form_html(self):
        form = ConversationThreadForm()

        form_html = form.as_p()

        self.assertFalse(form.is_bound)
        self.assertNotIn("Conversation Created By", form_html)
        self.assertNotIn("Conversation Modified By", form_html)
        self.assertIn("Conversation Name", form_html)
        self.assertIn("Conversation AI Models", form_html)
        self.assertIn("4o", form_html)

    def test_create_conversationthread_form_validation_blank_name_aimodel(self):
        form = ConversationThreadForm(
            data={
                "name": "",
                "aimodel": "",
            }
        )
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {
                "name": ["This field is required."],
                "aimodel": ["This field is required."],
            },
        )

    def test_create_conversationthread_form_validation_ok(self):
        form = ConversationThreadForm(
            data={
                "name": "Test Conversation",
                "aimodel": self.ai_model.id,
            }
        )
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
        self.assertDictEqual(form.errors, {})


@tag("form")
class CreateConversationItemFormTest(UserSetupMixin, TestCase):
    """
    This class performs basic tests for the ConversationItem Create Form.

    Attributes:

    methods:
        setUp
        test_create_conversationitem_form_html
        test_create_conversationitem_form_validation_blank_fields
        test_create_conversationitem_form_validation_ok
        test_create_conversationitem_form_for_duplicate_conversationitem_fieldnottobeduplicated_same_conversationthread
        test_create_conversationitem_form_for_duplicate_conversationitem_fieldnottobeduplicated_different_conversationthread
    """

    def setUp(self):
        super().setUp()
        self.ai_model = create_ai_model(
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
        self.conversation_thread = create_conversation_thread(
            self.user1, "Test Thread", "Test Summary", "web", self.ai_model
        )

    def test_create_conversation_item_form_html(self):
        conversation_thread_item = create_conversation_item(
            self.user1, self.conversation_thread, "", "", 1, 0
        )

        form = ConversationItemForm(instance=conversation_thread_item)

        form_html = form.as_p()

        self.assertFalse(form.is_bound)
        self.assertIn(
            'name="prompt" cols="40" rows="3" class="form-control form-control-lg" placeholder="What do you want to do?" required id="id_prompt"',
            form_html,
        )
        self.assertIn(
            f'input type="hidden" name="conversation_thread" value="{self.conversation_thread.id}" id="id_conversation_thread"',
            form_html,
        )
        self.assertIn(
            'input type="hidden" name="ORDER" value="0" id="id_ORDER"',
            form_html,
        )

    def test_create_conversation_item_form_validation_ok(self):
        conversation_thread_item = create_conversation_item(
            self.user1, self.conversation_thread, "", "", 1, 0
        )

        form = ConversationItemForm(
            {
                "prompt": "Prompt",
                "conversation_thread": conversation_thread_item.conversation_thread.id,
                "ORDER": conversation_thread_item.ORDER,
            },
        )

        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
        self.assertDictEqual(form.errors, {})

    def test_create_conversation_item_form_validation_blank_fields(self):
        # conversation_thread_item = create_conversation_item(
        #     self.user1, self.conversation_thread, "", "", 1, 0
        # )

        form = ConversationItemForm(
            {
                "prompt": "",
                "conversation_thread": self.conversation_thread.id,
                "ORDER": 0,
            },
        )
        # form.instance.a_conversationthread = a_conversationthread

        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {
                "prompt": ["required. A prompt must be posted."],
            },
        )


@tag("form")
class UpdateConversationItemFormTest(UserSetupMixin, TestCase):
    """
    This class performs basic tests for the ListItem Update Form.

    Attributes:

    methods:
        setUp
        test_update_conversationitem_form_html
        test_update_conversationitem_form_validation_blank_fields
        test_update_conversationitem_form_validation_ok
        test_update_conversationitem_form_for_duplicate_list_name_same_list
        test_update_conversationitem_form_for_duplicate_list_name_different_list
    """

    def setUp(self):
        super().setUp()
        self.ai_model = create_ai_model(
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
        self.conversation_thread = create_conversation_thread(
            self.user1, "Test Thread", "Test Summary", "web", self.ai_model
        )

    def test_update_conversation_item_form_validation_ok(self):
        conversation_thread_item1 = create_conversation_item(
            self.user1, self.conversation_thread, "Prompt1", "Response1", 1, 0
        )
        conversation_thread_item2 = create_conversation_item(
            self.user1, self.conversation_thread, "Prompt1", "Response1", 1, 1
        )
        conversation_threads = ConversationThread.objects.all()
        conversation_items = conversation_threads[0].conversation_items.all()
        self.assertEqual("Prompt1", conversation_items[0].prompt)

        form = ConversationItemForm(
            {
                "prompt": "Prompt1 has changed",
                "conversation_thread": conversation_thread_item1.conversation_thread.id,
                "ORDER": conversation_thread_item1.ORDER,
            },
            instance=conversation_thread_item1,
        )

        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
        self.assertDictEqual(form.errors, {})

        form.save()
        conversation_threads = ConversationThread.objects.all()
        conversation_items = conversation_threads[0].conversation_items.all()
        self.assertEqual("Prompt1 has changed", conversation_items[0].prompt)

    def test_update_conversation_item_form_validation_blank_fields(self):
        conversation_thread_item1 = create_conversation_item(
            self.user1, self.conversation_thread, "Prompt1", "Response1", 1, 0
        )
        conversation_thread_item2 = create_conversation_item(
            self.user1, self.conversation_thread, "Prompt1", "Response1", 1, 1
        )
        conversation_threads = ConversationThread.objects.all()
        conversation_items = conversation_threads[0].conversation_items.all()
        self.assertEqual("Prompt1", conversation_items[0].prompt)

        form = ConversationItemForm(
            {
                "prompt": "",
                "conversation_thread": conversation_thread_item1.conversation_thread.id,
                "ORDER": conversation_thread_item1.ORDER,
            },
            instance=conversation_thread_item1,
        )

        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertDictEqual(
            form.errors,
            {
                "prompt": ["required. A prompt must be posted."],
            },
        )


@tag("form")
class CreateConversationItemFormsetTest(UserSetupMixin, TestCase):
    """
    This class performs basic tests for the ConversationItem Formset.

    Attributes:

    methods:
        setUp
        test_create_conversationitem_formset_html
        test_create_conversationitem_formset_validation_blank_fields
        test_create_conversationitem_formset_validation_ok
        test_create_conversationitem_formset_for_duplicate_conversationitem_fieldnottobeduplicated_same_conversationthread
        test_create_conversationitem_formset_for_duplicate_conversationitem_fieldnottobeduplicated_different_conversationthread
    """

    def setUp(self):
        super().setUp()
        self.ai_model = create_ai_model(
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
        self.conversation_thread = create_conversation_thread(
            self.user1, "Test Thread", "Test Summary", "web", self.ai_model
        )

    def test_create_conversation_item_formset_html(self):
        conversation_thread_item1 = create_conversation_item(
            self.user1, self.conversation_thread, "Prompt1", "Response1", 1, 0
        )
        formset = ConversationItemFormset(
            queryset=ConversationItem.objects.none(),
            prefix="conversation_item",
            instance=self.conversation_thread,
        )

        for index, form in enumerate(formset):
            form_html = form.as_p()

            self.assertFalse(form.is_bound)
            self.assertIn(
                f'name="conversation_item-{index}-prompt" cols="40" rows="3" class="form-control form-control-lg" placeholder="What do you want to do?" id="id_conversation_item-{index}-prompt"',
                form_html,
            )
            self.assertIn(
                f'type="hidden" name="conversation_item-{index}-conversation_thread" value="{self.conversation_thread.id}" id="id_conversation_item-{index}-conversation_thread"',
                form_html,
            )
            self.assertIn(
                f'input type="number" name="conversation_item-{index}-ORDER" id="id_conversation_item-{index}-ORDER"',
                form_html,
            )
            self.assertIn(
                f'input type="checkbox" name="conversation_item-{index}-DELETE" id="id_conversation_item-{index}-DELETE"',
                form_html,
            )

    def test_create_conversation_item_formset_validation_ok(self):

        formset = ConversationItemFormset(
            data={
                "conversation_item-INITIAL_FORMS": "0",
                "conversation_item-TOTAL_FORMS": "1",
                "conversation_item-0-prompt": "Prompt 1",
                "conversation_item-0-conversation_thread": self.conversation_thread.id,
                "conversation_item-0-ORDER": 0,
            },
            prefix="conversation_item",
            instance=self.conversation_thread,
        )
        self.assertTrue(formset.is_valid())
        self.assertListEqual(formset.errors, [{}])
        formset.save()
        conversation_threads = ConversationThread.objects.all()
        conversation_items = conversation_threads[0].conversation_items.all()
        self.assertEqual(1, conversation_items.count())
        self.assertEqual("Prompt 1", conversation_items[0].prompt)

    def test_create_conversation_item_formset_validation_blank_fields(self):

        formset = ConversationItemFormset(
            data={
                "conversation_item-INITIAL_FORMS": "0",
                "conversation_item-TOTAL_FORMS": "1",
                "conversation_item-0-prompt": "",
                "conversation_item-0-conversation_thread": self.conversation_thread.id,
                "conversation_item-0-ORDER": 0,
            },
            prefix="conversation_item",
            instance=self.conversation_thread,
        )

        self.assertFalse(formset.is_valid())
        self.assertListEqual(
            formset.errors,
            [
                {
                    "prompt": ["required. A prompt must be posted."],
                }
            ],
        )


@tag("form")
class UpdateConversationItemFormsetTest(UserSetupMixin, TestCase):
    """
    This class performs basic tests for the ListItem Create Form.

    Attributes:

    methods:
        setUp
        test_update_conversationitem_formset_html
        test_update_conversationitem_formset_validation_blank_fields
        test_update_conversationitem_formset_validation_ok
        test_update_conversationitem_formset_for_duplicate_list_name_same_list
        test_update_conversationitem_formset_for_duplicate_list_name_different_list
    """

    def setUp(self):
        super().setUp()
        self.ai_model = create_ai_model(
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
        self.conversation_thread = create_conversation_thread(
            self.user1, "Test Thread", "Test Summary", "web", self.ai_model
        )

    def test_update_conversation_item_formset_html(self):
        conversation_thread_item1 = create_conversation_item(
            self.user1, self.conversation_thread, "Prompt1", "Response1", 1, 0
        )
        formset = ConversationItemFormset(
            queryset=ConversationItem.objects.none(),
            prefix="conversation_item",
            instance=self.conversation_thread,
        )

        for index, form in enumerate(formset):
            form_html = form.as_p()

            self.assertFalse(form.is_bound)
            self.assertIn(
                f'name="conversation_item-{index}-prompt" cols="40" rows="3" class="form-control form-control-lg" placeholder="What do you want to do?" id="id_conversation_item-{index}-prompt"',
                form_html,
            )
            self.assertIn(
                f'type="hidden" name="conversation_item-{index}-conversation_thread" value="{self.conversation_thread.id}" id="id_conversation_item-{index}-conversation_thread"',
                form_html,
            )
            self.assertIn(
                f'input type="number" name="conversation_item-{index}-ORDER" id="id_conversation_item-{index}-ORDER"',
                form_html,
            )
            self.assertIn(
                f'input type="checkbox" name="conversation_item-{index}-DELETE" id="id_conversation_item-{index}-DELETE"',
                form_html,
            )

    def test_update_conversationitem_formset_validation_ok(self):
        conversation_thread_item1 = create_conversation_item(
            self.user1, self.conversation_thread, "Prompt1", "Response1", 1, 0
        )
        conversation_thread_item2 = create_conversation_item(
            self.user1, self.conversation_thread, "Prompt1", "Response1", 1, 0
        )

        conversation_threads = ConversationThread.objects.all()
        conversation_items = conversation_threads[0].conversation_items.all()
        conversation_thread_item1 = conversation_items[0]
        self.assertEqual("Prompt1", conversation_thread_item1.prompt)

        formset = ConversationItemFormset(
            data={
                "conversation_item-INITIAL_FORMS": "1",
                "conversation_item-TOTAL_FORMS": "1",
                "conversation_item-0-id": conversation_thread_item1.id,
                "conversation_item-0-prompt": f"{conversation_thread_item1.prompt} has changed",
                "conversation_item-0-conversation_thread": conversation_thread_item1.conversation_thread.id,
                "conversation_item-0-ORDER": conversation_thread_item1.ORDER,
            },
            prefix="conversation_item",
            instance=self.conversation_thread,
        )

        self.assertTrue(formset.is_valid())
        formset.save()
        conversation_threads = ConversationThread.objects.all()
        conversation_items = conversation_threads[0].conversation_items.all()
        self.assertEqual(
            "Prompt1 has changed",
            conversation_items[0].prompt,
        )

    def test_update_conversationitem_formset_validation_blank_fields(self):
        conversation_thread_item1 = create_conversation_item(
            self.user1, self.conversation_thread, "Prompt1", "Response1", 1, 0
        )
        conversation_thread_item2 = create_conversation_item(
            self.user1, self.conversation_thread, "Prompt1", "Response1", 1, 0
        )

        conversation_threads = ConversationThread.objects.all()
        conversation_items = conversation_threads[0].conversation_items.all()
        conversation_thread_item1 = conversation_items[0]
        self.assertEqual("Prompt1", conversation_thread_item1.prompt)

        formset = ConversationItemFormset(
            data={
                "conversation_item-INITIAL_FORMS": "1",
                "conversation_item-TOTAL_FORMS": "1",
                "conversation_item-0-id": conversation_thread_item1.id,
                "conversation_item-0-prompt": "",
                "conversation_item-0-conversation_thread": conversation_thread_item1.conversation_thread.id,
                "conversation_item-0-ORDER": conversation_thread_item1.ORDER,
            },
            prefix="conversation_item",
            instance=self.conversation_thread,
        )

        self.assertFalse(formset.is_valid())
        self.assertListEqual(
            formset.errors,
            [
                {
                    "prompt": ["required. A prompt must be posted."],
                }
            ],
        )
