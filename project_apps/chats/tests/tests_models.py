"""This module unit tests the model for the chats app.

It has the test cases:
    ConversationThreadModelCRUDTest: This ensures that basic CRUD actions can be taken on the ConversationThread model.
    ConversationThreadModelValidationTest: This ensures that a ConversationThread model is validated as required. Also enforces some model best practice (e.g. get_absolute_url).
    ConversationItemModelCRUDTest: This ensures that basic CRUD actions can be taken on the ConversationItem model.
    ConversationItemModelValidationTest: This ensures that a ConversationItem model is validated as required. Also enforces some model best practice (e.g. get_absolute_url).

There are also 3 helper functions that are used by these tests but can also be imported into other tests.
    create_conversationthread
        Useage:
            from project_apps.chats.tests.tests_models import create_conversationthread

            create_conversationthread(user, name, summary, chat_type, aimodel)

    create_conversation_item
        Useage:
            from project_apps.chats.tests.tests_models import create_conversation_item

            src_conversation_thread = create_conversationthread(user, name, summary, chat_type, aimodel)
            create_conversation_item(user, src_conversation_thread, prompt, response, tokens, ORDER)

    create_conversation_items
        Useage:
            from project_apps.lists.tests.tests_models import create_conversation_items

            src_conversation_thread = create_conversationthread(user, name, summary, chat_type, aimodel)
            create_conversation_items(user, src_conversation_thread)

"""

from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase, tag

from project_apps.aimodels.tests.tests_models import create_ai_model
from project_apps.chats.models import ConversationItem, ConversationThread
from standard.tests.utils import UserSetupMixin


def create_conversation_thread(user, name, summary, chat_type, aimodel):
    """
    This is a helper function that creates a ConversationThread

    args:
        user: who created the conversationthread
        field1: field1 for the conversationitem

    returns:
        conversationthread: an instance of the a_ConversationThread model
    """
    conversation_thread = ConversationThread(
        name=name,
        summary=summary,
        chat_type=chat_type,
        created_by=user,
        modified_by=user,
        aimodel=aimodel,
    )
    conversation_thread.save()
    return conversation_thread


def create_conversation_item(
    user, src_conversation_thread, prompt, response, tokens=1, ORDER=0
):
    """
    This is a helper function that creates a ConversationItem

    args:
        user: who created the conversationitem
        target_conversationthread: The target_ConversationThread this ConversationItem will be a part of.
        field1: field1 for the ConversationItem

    returns:
        conversationitem: an instance of the a_ConversationItem model
    """
    conversation_item = ConversationItem(
        conversation_thread=src_conversation_thread,
        prompt=prompt,
        response=response,
        tokens=tokens,
        ORDER=ORDER,
        created_by=user,
        modified_by=user,
    )
    conversation_item.save()
    return conversation_item


def create_conversation_items(user, src_conversation_thread):
    """
    This is a helper function that creates a set of ConversationItem for a ConversationThread.

    args:
        user: who created the conversationitem
        target_conversationthread: the conversationthread this conversationitem will be a part of (an instance of the ConversationThread model)

    returns:
        None
    """
    create_conversation_item(
        user,
        src_conversation_thread,
        "Prompt 1",
        "Response 1",
        tokens=1,
        ORDER=0,
    )
    create_conversation_item(
        user,
        src_conversation_thread,
        "Prompt 2",
        "Response 2",
        tokens=2,
        ORDER=1,
    )
    create_conversation_item(
        user,
        src_conversation_thread,
        "Prompt 3",
        "Response 3",
        tokens=3,
        ORDER=2,
    )
    create_conversation_item(
        user,
        src_conversation_thread,
        "Prompt 4",
        "Response 4",
        tokens=4,
        ORDER=3,
    )
    create_conversation_item(
        user,
        src_conversation_thread,
        "Prompt 5",
        "Response 5",
        tokens=5,
        ORDER=4,
    )


@tag("model")
class TestConversationThreadModelValidation(UserSetupMixin, TestCase):
    """
    This class tests validation against constrained attributes of the ConversationThread model

    Attributes:

    methods:
        setUp
        test_conversationthread_verbose_name_and_verbose_name_plural
        test_conversationthread_class_string_set
        test_conversationthread_get_absolute_url
        test_conversationthread_field_verbose_name
        test_conversationthread_choices
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

    def test_conversation_thread_verbose_name_and_verbose_name_plural(self):
        """
        This function tests that the ConversationThread model has verbose name and verbose name plural set.

        args:

        returns:
        """
        self.assertEqual(ConversationThread._meta.verbose_name_raw, "Chat")
        self.assertEqual(ConversationThread._meta.verbose_name_plural, "Chats")

    def test_conversationthread_class_string_set(self):
        """
        This function tests that the ConversationThread model has a __string__ set.

        args:

        returns:
        """
        conversation_thread = create_conversation_thread(
            self.user1,
            "Name for the thread",
            "Summary for the thread",
            "web",
            self.ai_model,
        )
        self.assertEqual(str(conversation_thread), conversation_thread.name)

    def test_conversationthread_get_absolute_url(self):
        """
        This function tests that the ConversationThread model has a get_absolute_url set.

        args:

        returns:
        """
        conversation_thread = create_conversation_thread(
            self.user1,
            "Name for the thread",
            "Summary for the thread",
            "web",
            self.ai_model,
        )
        self.assertEqual(
            conversation_thread.get_absolute_url(),
            f"/chats/{ conversation_thread.id}/",
        )

    def test_conversationthread_field_verbose_name(self):
        """
        This function tests that the ConversationThread model's fields have verbose name set.

        args:

        returns:
        """
        self.assertEqual(
            ConversationThread._meta.get_field("name").verbose_name.title(),
            "Conversation Name",
        )
        self.assertEqual(
            ConversationThread._meta.get_field("summary").verbose_name.title(),
            "Conversation Summary",
        )
        self.assertEqual(
            ConversationThread._meta.get_field("chat_type").verbose_name.title(),
            "Conversation Type",
        )
        self.assertEqual(
            ConversationThread._meta.get_field("aimodel").verbose_name.title(),
            "Conversation Ai Models",
        )
        self.assertEqual(
            ConversationThread._meta.get_field("created_by").verbose_name.title(),
            "Conversation Created By",
        )
        self.assertEqual(
            ConversationThread._meta.get_field("created_at").verbose_name.title(),
            "Conversation Created At",
        )
        self.assertEqual(
            ConversationThread._meta.get_field("modified_by").verbose_name.title(),
            "Conversation Modified By",
        )
        self.assertEqual(
            ConversationThread._meta.get_field("modified_at").verbose_name.title(),
            "Conversation Modified At",
        )

    def test_conversationthread_has_required_field(self):
        """
        This function tests that there must be text data for an instance of ConversationThread
        ...and if not throws a ValidationError

        args:

        returns:
        """
        conversation_thread = create_conversation_thread(
            self.user1, "", "Summary for the thread", "web", self.ai_model
        )

        with self.assertRaises(ValidationError):
            conversation_thread.full_clean()

        conversation_thread = create_conversation_thread(
            self.user1,
            "Name for the thread",
            "Summary for the thread",
            "",
            self.ai_model,
        )

        with self.assertRaises(ValidationError):
            conversation_thread.full_clean()

    def test_conversationthread_choices(self):
        self.assertTupleEqual(
            ConversationThread.THREAD_TYPES[0],
            ("web", "Web"),
            "Missing the Web option",
        )

        self.assertTupleEqual(
            ConversationThread.THREAD_TYPES[1],
            ("api", "API"),
            "Missing the API option",
        )

        self.assertTupleEqual(
            ConversationThread.THREAD_TYPES[2],
            ("noa", "NOA"),
            "Missing the NOA option",
        )


@tag("model")
class ConversationThreadModelCRUDTest(UserSetupMixin, TestCase):
    """
    This class performs basic CRUD tests for the ConversationThread Model

    Attributes:

    methods:
        setUp
        test_saving_and_retrieving_conversationthreads
        test_modifying_conversationthread
        test_deleting_conversationthread
        test_effect_of_deleting_user_on_conversationthread
        test_conversationthread_DISALLOW_duplicate_name
        _check_conversationthread
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

    def _check_conversation_thread(
        self, target_conversation_thread, name, summary, chat_type, user
    ):
        """
        This function attempts a number of assertions against a ConversationThread

        args:

        returns:
        """
        self.assertEqual(target_conversation_thread.name, name)
        self.assertEqual(target_conversation_thread.summary, summary)
        self.assertEqual(target_conversation_thread.chat_type, chat_type)
        self.assertEqual(target_conversation_thread.created_by, user)
        self.assertEqual(target_conversation_thread.created_at, date.today())

    def test_saving_and_retrieving_conversationthreads(self):
        """
        This function tests creating a ConversationThread and then retrieving it.

        args:

        returns:
        """
        create_conversation_thread(
            self.user1,
            "Name for the thread 1",
            "Summary for the thread 1",
            "web",
            self.ai_model,
        )
        create_conversation_thread(
            self.user2,
            "Name for the thread 2",
            "Summary for the thread 2",
            "api",
            self.ai_model,
        )

        saved_conversationthreads = ConversationThread.objects.all()
        first_saved_conversationthread = saved_conversationthreads[0]
        second_saved_conversationthread = saved_conversationthreads[1]

        self._check_conversation_thread(
            first_saved_conversationthread,
            "Name for the thread 1",
            "Summary for the thread 1",
            "web",
            self.user1,
        )

        self._check_conversation_thread(
            second_saved_conversationthread,
            "Name for the thread 2",
            "Summary for the thread 2",
            "api",
            self.user2,
        )

    def test_modifying_conversationthread(self):
        """
        This function tests making changes to a ConversationThread

        args:

        returns:
        """
        create_conversation_thread(
            self.user1,
            "Name for the thread 1",
            "Summary for the thread 1",
            "web",
            self.ai_model,
        )

        saved_conversationthreads = ConversationThread.objects.all()
        first_saved_conversationthread = saved_conversationthreads[0]
        first_saved_conversationthread.name = "Changed value for name"
        first_saved_conversationthread.modified_by = self.user1
        first_saved_conversationthread.save()

        saved_conversationthreads = ConversationThread.objects.all()
        first_saved_conversationthread = saved_conversationthreads[0]
        self.assertEqual(first_saved_conversationthread.name, "Changed value for name")
        self.assertEqual(first_saved_conversationthread.modified_by, self.user1)
        self.assertEqual(first_saved_conversationthread.modified_at, date.today())

    def test_deleting_conversationthread(self):
        """
        This function tests deleting a ConversationThread

        args:

        returns:
        """
        create_conversation_thread(
            self.user1,
            "Name for the thread 1",
            "Summary for the thread 1",
            "web",
            self.ai_model,
        )

        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 1)
        first_saved_conversationthread = saved_conversationthreads[0]
        first_saved_conversationthread.delete()

        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 0)

    def test_effect_of_deleting_user_on_conversationthread(self):
        """
        This function tests what happens to a ConversationThread if a user is deleted
        It should still exist in the database

        args:

        returns:
        """
        create_conversation_thread(
            self.user2,
            "Name for the thread 1",
            "Summary for the thread 1",
            "web",
            self.ai_model,
        )

        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 1)
        self.assertEqual(saved_conversationthreads[0].created_by, self.user2)

        saved_users = get_user_model().objects.all()
        self.assertEqual(saved_users.count(), 2)
        self.user2.delete()
        saved_users = get_user_model().objects.all()
        self.assertEqual(saved_users.count(), 1)

        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 1)
        self.assertNotEqual(saved_conversationthreads[0].created_by, self.user2)


@tag("model")
class ConversationItemModelValidationTest(UserSetupMixin, TestCase):
    """
    This class tests validation of constrained attributes of the ListItem model

    Attributes:

    methods:
        setUp
        test_conversationitem_verbose_name_and_verbose_name_plural
        test_conversationitem_class_string_set
        test_conversationitem_get_absolute_url
        test_conversationitem_field_verbose_name
        test_conversationitem_has_text
        test_conversationitem_attached_to_a_list
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
            self.user1,
            "Name for the thread 1",
            "Summary for the thread 1",
            "web",
            self.ai_model,
        )

    def test_conversation_item_verbose_name_and_verbose_name_plural(self):
        """
        This function tests that the ConversationItem model has verbose name and verbose name plural set.

        args:

        returns:
        """
        self.assertEqual(ConversationItem._meta.verbose_name_raw, "Conversation Item")
        self.assertEqual(
            ConversationItem._meta.verbose_name_plural, "Conversation Items"
        )

    def test_conversation_item_class_string_set(self):
        """
        This function tests that the ConversationItem model has a __string__ set.

        args:

        returns:
        """
        conversation_thread1 = create_conversation_item(
            self.user1,
            self.conversation_thread,
            "Prompt 1",
            "Response 1",
            tokens=1,
            ORDER=0,
        )

        self.assertEqual(
            str(conversation_thread1),
            "Item for chat Name for the thread 1 created by junior, modified by junior and used 1 tokens",
        )

    def test_conversation_item_get_absolute_url(self):
        """
        This function tests that the ConversationItem model has a get_absolute_url set.

        args:

        returns:
        """
        conversation_thread1 = create_conversation_item(
            self.user1,
            self.conversation_thread,
            "Prompt 1",
            "Response 1",
            tokens=1,
            ORDER=0,
        )
        conversation_thread2 = create_conversation_item(
            self.user1,
            self.conversation_thread,
            "Prompt 2",
            "Response 2",
            tokens=1,
            ORDER=1,
        )
        self.assertEqual(
            conversation_thread2.get_absolute_url(),
            f"/chats/{conversation_thread2.conversation_thread.id}/",
        )

    def test_conversation_item_field_verbose_name(self):
        """
        This function tests that the ConversationItem model's fields have verbose name set.

        args:

        returns:
        """
        self.assertEqual(
            ConversationItem._meta.get_field(
                "conversation_thread"
            ).verbose_name.title(),
            "Conversation Items",
        )
        self.assertEqual(
            ConversationItem._meta.get_field("prompt").verbose_name.title(),
            "Conversation'S Item'S Prompt",
        )
        self.assertEqual(
            ConversationItem._meta.get_field("response").verbose_name.title(),
            "Conversation'S Item'S Response",
        )
        self.assertEqual(
            ConversationItem._meta.get_field("tokens").verbose_name.title(), "Tokens"
        )
        self.assertEqual(
            ConversationItem._meta.get_field("is_full_saved").verbose_name.title(),
            "Is Full Saved",
        )
        self.assertEqual(
            ConversationItem._meta.get_field("created_by").verbose_name.title(),
            "Chats Item Created By",
        )
        self.assertEqual(
            ConversationItem._meta.get_field("created_at").verbose_name.title(),
            "Chats Item Created At",
        )
        self.assertEqual(
            ConversationItem._meta.get_field("modified_by").verbose_name.title(),
            "Chats Item Modified By",
        )
        self.assertEqual(
            ConversationItem._meta.get_field("modified_at").verbose_name.title(),
            "Chats Item Modified At",
        )
        self.assertEqual(
            ConversationItem._meta.get_field("ORDER").verbose_name.title(),
            "Order In Chats",
        )

    def test_conversation_item_has_required_fields(self):
        """
        This function tests that there must be text data for an instance of ConversationItem
        ...and if not throws a ValidationError

        args:

        returns:
        """
        conversation_thread1 = create_conversation_item(
            self.user1,
            self.conversation_thread,
            "",
            "Response 1",
            tokens=1,
            ORDER=0,
        )

        with self.assertRaises(ValidationError):
            conversation_thread1.full_clean()

        conversation_thread1 = create_conversation_item(
            self.user1,
            self.conversation_thread,
            "Prompt 1",
            "",
            tokens=1,
            ORDER=0,
        )

        with self.assertRaises(ValidationError):
            conversation_thread1.full_clean()

    def test_conversation_item_attached_to_a_conversationthread(self):
        """
        This function tests that an instance of ConversationItem is linked to
        an instance of ConversationThread ...and if it doesn't throws an integrity error
        This requires a blank=False and null=False in connection field attribute declaration.

        args:

        returns:
        """
        conversation_thread1 = ConversationItem(
            conversation_thread=None,
            prompt="Prompt1",
            response="Response 1",
            tokens=1,
            ORDER=0,
            created_by=self.user1,
            modified_by=self.user1,
        )

        with self.assertRaises(ValidationError):
            conversation_thread1.full_clean()


@tag("model")
class ConversationItemModelCRUDTest(UserSetupMixin, TestCase):
    """
    This class performs basic CRUD tests for the ListItem model

    Attributes:

    methods:
        setUp
        test_saving_and_retrieving_conversationthread_and_conversationitems
        test_modifying_a_conversationthreads_conversationitem
        test_deleting_a_conversationitem
        test_effect_of_deleting_a_conversationthread_on_conversationitems
        test_conversationitem_DISALLOW_duplicate_text_in_same_conversationthread
        test_conversationitem_ALLOW_duplicate_text_in_different_conversationthreads
        _check_conversationitem
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
            self.user1,
            "Name for the thread 1",
            "Summary for the thread 1",
            "web",
            self.ai_model,
        )

    def _check_conversation_item(self, conversation_item, prompt):
        """
        This function attempts a number of assertaions on a ConversationItem

        args:

        returns:
        """
        self.assertEqual(conversation_item.prompt, prompt)
        self.assertEqual(conversation_item.created_by, self.user1)
        self.assertEqual(conversation_item.created_at, date.today())

    def test_saving_and_retrieving_conversationthread_and_conversationitems(self):
        """
        This function tests creating, saving and retrieving a ConversationItem

        args:

        returns:
        """

        conversation_thread_item1 = create_conversation_item(
            self.user1,
            self.conversation_thread,
            "Prompt 1",
            "Response 1",
            tokens=1,
            ORDER=0,
        )
        conversation_thread_item2 = create_conversation_item(
            self.user1,
            self.conversation_thread,
            "Prompt 2",
            "Response 2",
            tokens=1,
            ORDER=0,
        )

        saved_conversation_threads = ConversationThread.objects.all()
        conversation_thread = saved_conversation_threads[0]
        conversationitems = conversation_thread.conversation_items.all()

        self.assertEqual(conversation_thread.name, "Name for the thread 1")

        self._check_conversation_item(conversationitems[0], "Prompt 1")
        self._check_conversation_item(conversationitems[1], "Prompt 2")

    def test_modifying_a_conversationthreads_conversationitem(self):
        """
        This function test the modifying of a ConversationItem

        args:

        returns:
        """
        conversation_thread_item1 = create_conversation_item(
            self.user1,
            self.conversation_thread,
            "Prompt 1",
            "Response 1",
            tokens=1,
            ORDER=0,
        )

        conversationitem = ConversationItem.objects.get(id=conversation_thread_item1.id)
        conversationitem.prompt = "Changed value"
        conversationitem.modified_by = self.user1
        conversationitem.save()

        conversationitem = ConversationItem.objects.get(id=conversation_thread_item1.id)
        self.assertEqual(conversationitem.prompt, "Changed value")
        self.assertEqual(conversationitem.modified_by, self.user1)
        self.assertEqual(conversationitem.modified_at, date.today())

    def test_deleting_a_conversationitem(self):
        """
        This function tests the deletion of a ConversationItem

        args:

        returns:
        """
        conversation_thread_item1 = create_conversation_item(
            self.user1,
            self.conversation_thread,
            "Prompt 1",
            "Response 1",
            tokens=1,
            ORDER=0,
        )

        conversation_threads = ConversationThread.objects.all()
        conversation_thread1 = conversation_threads[0]
        conversation_items = conversation_thread1.conversation_items.all()
        self.assertEqual(conversation_items.count(), 1)

        conversationitem = ConversationItem.objects.get(id=conversation_items[0].id)
        conversationitem.delete()

        conversation_threads = ConversationThread.objects.all()
        conversation_thread1 = conversation_threads[0]
        conversation_items = conversation_thread1.conversation_items.all()
        self.assertEqual(conversation_items.count(), 0)

    def test_effect_of_deleting_a_conversationthread_on_conversationitems(self):
        """
        This function tests what happens when a ConversationThread is deleted
        The ConversationItem should also be deleted.

        args:

        returns:
        """
        conversation_thread_item1 = create_conversation_item(
            self.user1,
            self.conversation_thread,
            "Prompt 1",
            "Response 1",
            tokens=1,
            ORDER=0,
        )

        conversation_threads = ConversationThread.objects.all()
        conversation_thread1 = conversation_threads[0]
        conversation_items = conversation_thread1.conversation_items.all()
        self.assertEqual(conversation_items.count(), 1)

        conversation_thread1.delete()

        conversation_threads = ConversationThread.objects.all()
        self.assertEqual(conversation_threads.count(), 0)

        conversation_thread_items = ConversationItem.objects.all()
        self.assertEqual(conversation_thread_items.count(), 0)
