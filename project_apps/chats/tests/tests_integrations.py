"""This module performs integration tests the chats app ensuring all aspects
of the apps development work together.

"""

from django.test import TestCase, override_settings, tag
from django.urls import reverse

from standard.tests.utils import UserSetupMixin


@tag("integration")
@override_settings(SECURE_SSL_REDIRECT=False)
class ConversationThreadTest(UserSetupMixin, TestCase):
    """
    This class performs basic tests of the chats app

    Attributes:

    methods:
        setUp
        test_views_of_conversationthread_not_logged_in

        test_view_empty_list_of_conversationthread
        test_view_list_of_conversationthread

        test_view_conversationthread_details_without_ConversationItem
        test_view_conversationthread_details_with_ConversationItem

        test_view_conversationthread_create_get
        test_view_conversationthread_create_no_ConversationItem
        test_view_conversationthread_create_with_ConversationItem
        test_view_conversationthread_create_DISALLOW_duplicate_conversationthread_fieldnottobeduplicated
        test_view_conversationthread_create_DISALLOW_duplicate_conversationitem_fieldnottobeduplicated_for_same_conversationthread
        test_view_conversationthread_create_ALLOW_duplicate_conversationitem_fieldnottobeduplicated_for_different_conversationthreads

        test_view_conversationitem_update_get
        test_view_conversationitem_update_with_conversationitems
        test_view_conversationthread_update_DISALLOW_duplicate_conversationthread_fieldnottobeduplicated
        test_view_conversationthread_update_DISALLOW_duplicate_conversationitem_fieldnottobeduplicated_for_same_conversationthread
        test_view_conversationthread_update_ALLOW_duplicate_conversationitem_fieldnottobeduplicated_for_different_conversationthreads
    """


''' SECTION 3
    Then work your way slowly through the tests modifying for your app
    def _get_response(self, user=None, url=None):
        if user is not None:
            self.client.force_login(user)

        return self.client.get(url, follow=True)

    def test_views_of_conversationthread_not_logged_in(self):
        """
        This function tests that the response for all conversationthread 
        views without a user being logged in.

        args:

        returns:
        """
        a_conversationthread = create_conversationthread(self.user1, field1, field2, field3)
        create_conversationthread(self.user1, field1, field2, field3)

        response = self._get_response(url=reverse("conversationthreads"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "PROJECT NAME Login")

        response = self._get_response(url=reverse("conversationthread_detail", kwargs={"pk": a_conversationthread.id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "PROJECT NAME Login")

        response = self.client.get(reverse("conversationthread_create"), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "PROJECT NAME Login")

        response = self.client.get(
            reverse("conversationthread_update", kwargs={"pk": a_conversationthread.id}), follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "PROJECT NAME Login")

    def test_view_empty_list_of_conversationthread(self):
        """
        This function tests a view where there are no existing conversationthread.

        args:

        returns:
        """
        response = self._get_response(self.user1, reverse("conversationthreads"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "PROJECT NAME - ConversationThreads")
        self.assertContains(response, "Welcome to ConversationThreads")
        self.assertContains(response, "There are no ConversationThreads")
        self.assertTemplateUsed("chats/chats.html")
        self.assertTemplateUsed("chats/list/chats_list_empty.html")

    def test_view_list_of_conversationthread(self):
        """
        This function tests a view that enables a user to view existing lists.

        args:

        returns:
        """
        create_conversationthread(self.user1, field1, field2, field3)
        create_conversationthread(self.user1, field1, field2, field3)
        response = self._get_response(self.user1, reverse("conversationthreads"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "PROJECT NAME - ConversationThreads")
        self.assertContains(response, "Welcome to ConversationThreads")
        self.assertContains(response, "Current ConversationThread")
        self.assertContains(response, "field1 from first ConversationThread")
        self.assertContains(response, "field1 from second ConversationThread")
        self.assertTemplateUsed("chats/chats.html")
        self.assertTemplateUsed("chats/list/chats_list.html")
        self.assertTemplateUsed("chats/list/chats_list_header.html")
        self.assertTemplateUsed("chats/list/chats_list_title.html")
        self.assertTemplateUsed("chats/list/chats_list_item.html")

    def test_view_conversationthread_details_without_conversationitems(self):
        """
        This function tests a view that enables a user to view an existing conversationthread's details.

        args:

        returns:
        """
        first_conversationthread = create_conversationthread(self.user1, field1, field2, field3)
        response = self._get_response(self.user1, first_conversationthread.get_absolute_url())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "PROJECT NAME - ConversationThread Details")
        self.assertContains(response, "Details for ConversationThread:")
        self.assertContains(response, "field1value")
        self.assertContains(response, "field2value")
        self.assertContains(response, "field3value")
        #self.assertContains(response, "ConversationThread's ConversationItem")
        #self.assertContains(response, "No ConversationItem")
        self.assertTemplateUsed("chats/chats_detail.html")
        self.assertTemplateUsed("chats/detail/chats_detail_item.html")
        self.assertTemplateUsed("chats/detail/chats_detail_header.html")
        self.assertTemplateUsed("chats/detail/chats_detail_multi_item_list.html")

    def test_view_conversationthread_create_get(self):
        response = self._get_response(self.user1, reverse("conversationthread_create"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "PROJECT NAME - ConversationThread Creation")
        self.assertContains(response, "Create New ConversationThread")
        self.assertContains(response, "field1 label")
        self.assertContains(response, "field2 label")
        self.assertContains(response, "field3 label")
        
    def test_view_conversationthread_create_no_conversationitems(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("conversationthread_create"),
            follow=True,
            data={
                "field1": "field1 value",
                "field2": "field2 value",
                "field3": "field3 value",
                #"conversationitem-INITIAL_FORMS": "0",
                #"conversationitem-TOTAL_FORMS": "0",
            },
        )

        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 1)
        #self.assertEqual(saved_conversationthreads[0].list_items.all().count(), 0)

    def test_view_conversationthread_create_DISALLOW_duplicate_conversationthread_fieldnottobeduplicated(self):
        first_conversationthread = create_conversationthread(self.user1, fieldnottobeduplicated, field2, field3)
        self.client.force_login(self.user1)
        response = self.client.post(
            "http://testserver/chats/create/",
            data={
                "fieldnottobeduplicated": "Duplicate value",
                "field2": "field2 value",
                "field3": "field3 value",
                "conversationitem-INITIAL_FORMS": "0",
                "conversationitem-TOTAL_FORMS": "2",
                "conversationitem-0-itemfield1": "itemfield1 value",
                "conversationitem-0-itemfield2": "itemfield2 value",
                "conversationitem-0-ORDER": 2,
                "conversationitem-1-itemfield1": "itemfield1 value",
                "conversationitem-1-itemfield2": "itemfield2 value",
                "conversationitem-1-ORDER": 1,
            },
        )

        self.assertContains(response, "The fieldnottobeduplicated for this ConversationThread already exists")
        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 1)

    def test_view_conversationthread_update_get(self):
        first_conversationthread = create_conversationthread(self.user1, field1, field2, field3)
        response = self._get_response(
            self.user1, 
            reverse("conversationthread_update", kwargs={"pk": first_conversationthread.id}),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "PROJECT NAME - ConversationThread Edit")
        self.assertContains(response, "Edit ConversationThread")
        self.assertContains(response, "field1 label")
        self.assertContains(response, "field2 label")
        self.assertContains(response, "field3 label")

    def test_view_conversationthread_update_DISALLOW_duplicate_conversationthread_fieldnottobeduplicated(self):
        first_conversationthread = create_conversationthread(self.user1, field1, field2, field3)
        second_conversationthread = create_conversationthread(self.user1, field1, field2, field3)

        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("conversationthread_update", kwargs={"pk": second_conversationthread.id}),
            follow=True,
            data={
                "_fieldnottobeduplicated": "field1 duplicate vale",
                "field2": second_conversationthread.field2,
                "field3": second_conversationthread.field3,
                "conversationitem-INITIAL_FORMS": "0",
                "conversationitem-TOTAL_FORMS": "0",
            },
        )

        self.assertContains(response, "The fieldnottobeduplicated value for this conversationthread already exists")

    def test_view_conversationthread_delete_get(self):
        first_conversationthread = create_conversationthread(self.user1, field1, field2, field3)
        response = self._get_response(
            self.user1,
            reverse("conversationthread_delete", kwargs={"pk": first_conversationthread.id}),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "PROJECT NAME - ConversationThread Delete")
        self.assertContains(response, "Delete ConversationThread")
        self.assertContains(response, "A Test ConversationThread")
        self.assertContains(response, "A(n) conversationthread for the purposes of testing")

    def test_view_conversationthread_delete_post(self):
        first_conversationthread = create_conversationthread(self.user1, field1, field2, field3)
        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 1)
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("conversationthread_delete", kwargs={"pk": first_conversationthread.id}),
            follow=True,
            data={},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 0)

    def test_view_conversationthread_details_with_conversationitems(self):
        """
        This function tests a view that enables a user to view an existing conversationthread's details.

        args:

        returns:
        """
        first_conversationthread = create_conversationthread(self.user1, field1, field2, field3)

        response = self._get_response(self.user1, first_conversationthread.get_absolute_url())

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "PROJECT NAME - ConversationThread Details")
        self.assertContains(response, "Details for ConversationThread:")
        self.assertContains(response, "field1value")
        self.assertContains(response, "field2value")
        self.assertContains(response, "field3value")
        self.assertContains(response, "ConversationThread's ConversationItem")
        self.assertContains(response, "The first ConversationItem")
        self.assertContains(response, "The fifth ConversationItem")
        self.assertTemplateUsed("chats/chats_detail.html")
        self.assertTemplateUsed("chats/detail/chats_detail_item.html")
        self.assertTemplateUsed("chats/detail/chats_detail_header.html")
        self.assertTemplateUsed("chats/detail/chats_detail_multi_item_list.html")

    def test_view_conversationthread_create_with_conversationitems(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            "http://testserver/chats/create/",
            follow=True,
            data={
                "field1": "field1 value",
                "field2": "field2 value",
                "field3": "field3 value",
                "conversationitem-INITIAL_FORMS": "0",
                "conversationitem-TOTAL_FORMS": "2",
                "conversationitem-0-itemfield1": "itemfield1 value",
                "conversationitem-0-itemfield2": "itemfield2 value",
                "conversationitem-0-ORDER": 2,
                "conversationitem-1-itemfield1": "itemfield1 value",
                "conversationitem-1-itemfield2": "itemfield2 value",
                "conversationitem-1-ORDER": 1,
            },
        )

        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 1)
        saved_conversationitems = saved_conversationthreads[0].list_items.all().order_by("ORDER")
        self.assertEqual(saved_conversationitems.count(), 2)
        self.assertEqual(saved_conversationitems[0].itemfield1, "itemfield1 value")

    def test_view_conversationthread_create_DISALLOW_duplicate_conversationitem_fieldnottobeduplicated_for_same_conversationthread(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            "http://testserver/chats/create/",
            data={
                "field1": "field1 value",
                "field2": "field2 value",
                "field3": "field3 value",
                "conversationitem-INITIAL_FORMS": "0",
                "conversationitem-TOTAL_FORMS": "2",
                "conversationitem-0-fieldnottobeduplicated": "fieldnottobeduplicated value",
                "conversationitem-0-itemfield2": "itemfield2 value",
                "conversationitem-0-ORDER": 2,
                "conversationitem-1-fieldnottobeduplicated": "fieldnottobeduplicated value",
                "conversationitem-1-itemfield2": "itemfield2 value",
                "conversationitem-1-ORDER": 1,
            },
        )

        self.assertContains(response, "conversationitem in a conversationthread must have distinct fieldnottobeduplicated")
        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 0)

    def test_view_conversationthread_create_ALLOW_duplicate_conversationitem_fieldnottobeduplicated_for_different_conversationthreads(self):
        first_conversationthread = create_conversationthread(self.user1, field1, field2, field3)
        create_conversationitems(self.user1, first_conversationthread)
        self.client.force_login(self.user1)
        response = self.client.post(
            "http://testserver/chats/create/",
            follow=True,
            data={
                "field1": "field1 value",
                "field2": "field2 value",
                "field3": "field3 value",
                "conversationitem-INITIAL_FORMS": "0",
                "conversationitem-TOTAL_FORMS": "2",
                "conversationitem-0-fieldnottobeduplicated": "fieldnottobeduplicated value",
                "conversationitem-0-itemfield2": "itemfield2 value",
                "conversationitem-0-ORDER": 2,
                "conversationitem-1-field1": "field1 value",
                "conversationitem-1-itemfield2": "itemfield2 value",
                "conversationitem-1-ORDER": 1,
            },
        )

        self.assertNotContains(response, "conversationitem in a conversationthread must have distinct fieldnottobeduplicated")
        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 2)

    def test_view_conversationthread_update_with_conversationitems(self):
        first_conversationthread = create_conversationthread(self.user1, field1, field2, field3)
        first_conversationitem = create_conversationitem(self.user1, first_conversationthread, field1, field2)
        second_conversationitem = create_conversationitem(self.user1, first_conversationthread, field1, field2)
        self.client.force_login(self.user1)        

        response = self.client.post(
            reverse("conversationthread_update", kwargs={"pk": first_conversationthread.id}),
            follow=True,
            data={
                "field1": "field1 new value",
                "field2": "field2 value",
                "field3": "field3 value",
                "conversationitem-INITIAL_FORMS": "0",
                "conversationitem-TOTAL_FORMS": "2",
                "conversationitem-0-itemfield1": "itemfield1 new value",
                "conversationitem-0-itemfield2": first_conversationitem.itemfield2,
                "conversationitem-0-ORDER": first_conversationitem.ORDER,
                "conversationitem-1-itemfield1":second_conversationitem.itemfield1,
                "conversationitem-1-itemfield2": second_conversationitem.itemfield2,
                "conversationitem-1-ORDER": second_conversationitem.ORDER,
            },
        )

        saved_conversationthreads = ConversationThread.objects.all()
        self.assertEqual(saved_conversationthreads.count(), 1)
        self.assertEqual(saved_conversationthreads[0].field1, "field1 new value")

        saved_conversationitems = saved_conversationthreads[0].list_items.all()
        self.assertEqual(saved_conversationitems.count(), 2)
        saved_conversationitems_text = [item.text for item in saved_conversationitems]
        self.assertIn("itemfield1 new value", saved_conversationitems_text)
        self.assertIn("itemfield1 value", saved_conversationitems_text)

    def test_view_conversationthread_update_DISALLOW_duplicate_conversationitem_fieldnottobeduplicated_for_same_conversationthread(self):
        first_conversationthread = create_conversationthread(self.user1, field1, field2, field3)
        first_conversationitem = create_conversationitem(self.user1, first_conversationthread, field1, field2)
        second_conversationitem = create_conversationitem(self.user1, first_conversationthread, field1, field2)

        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("conversationthread_update", kwargs={"pk": first_conversationthread.id}),
            follow=True,
            data={
                "field1": "field1 value",
                "field2": "field2 value",
                "field3": "field3 value",
                "conversationitem-INITIAL_FORMS": "2",
                "conversationitem-TOTAL_FORMS": "2",
                "conversationitem-0-fieldnottobeduplicated": "fieldnottobeduplicated value",
                "conversationitem-0-itemfield2": "itemfield2 value",
                "conversationitem-0-ORDER": 2,
                "conversationitem-1-field1": "field1 value",
                "conversationitem-1-itemfield2": "itemfield2 value",
                "conversationitem-1-ORDER": 1,
            },
        )

        self.assertContains(response, "conversationitem in a conversationthread must have distinct fieldnottobeduplicated")

    def test_view_conversationthread_update_ALLOW_duplicate_conversationitem_fieldnottobeduplicated_for_different_conversationthreads(self):
        first_conversationthread = create_conversationthread(self.user1, field1, field2, field3)
        create_conversationitems(self.user1, first_conversationthread)
        second_conversationthread = create_conversationthread(self.user1, field1, field2, field3)
        first_conversationitem = create_conversationitem(self.user1, first_conversationthread, field1, field2)
        second_conversationitem = create_conversationitem(self.user1, first_conversationthread, field1, field2)

        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("conversationthread_update", kwargs={"pk": test_list.id}),
            follow=True,
            data={
                "field1": "field1 value",
                "field2": "field2 value",
                "field3": "field3 value",
                "conversationitem-INITIAL_FORMS": "2",
                "conversationitem-TOTAL_FORMS": "2",
                "conversationitem-0-id": first_conversationitem.id,
                "conversationitem-0-fieldnottobeduplicated": "fieldnottobeduplicated value",
                "conversationitem-0-itemfield2": first_conversationitem.field2,
                "conversationitem-0-ORDER": first_conversationitem.ORDER,
                "conversationitem-1-id": second_conversationitem.id,
                "conversationitem-1-field1": second_conversationitem.field1,
                "conversationitem-1-itemfield2": second_conversationitem.field2,
                "conversationitem-1-ORDER": second_conversationitem.ORDER,
            },
        )

        self.assertNotContains(response, "conversationitem in a conversationthread must have distinct fieldnottobeduplicated")
'''
