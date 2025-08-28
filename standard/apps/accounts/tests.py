from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse, reverse_lazy

from standard.tests.models import ModelTestMixin


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="max@anaddress.com",
            username="max",
            password="testpass123",
            address1="address line 1",
            address2="address line 2",
            address3="address line 3",
            address4="address line 4",
            terms_and_conditions=False,
        )
        """ Create user with additional fields 
            staff_number="123",
            phone="+44 7800 000 000",
            emergency_first_name="Their",
            emergency_last_name="Mumsy",
            emergency_email="mumsy@anaddress.co.uk",
            emergency_phone="+44 7800 000 001",
        """

        self.assertEqual(user.username, "max")
        self.assertEqual(user.email, "max@anaddress.com")
        self.assertEqual(user.address1, "address line 1")
        self.assertEqual(user.address2, "address line 2")
        self.assertEqual(user.address3, "address line 3")
        self.assertEqual(user.address4, "address line 4")
        self.assertFalse(user.terms_and_conditions)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        """ add extra field tests as appropriate
        self.assertEqual(user.staff_number, "123")
        self.assertEqual(user.phone, "+44 7800 000 000")
        self.assertEqual(user.emergency_first_name, "Their")
        self.assertEqual(user.emergency_last_name, "Mumsy")
        self.assertEqual(user.emergency_email, "mumsy@anaddress.co.uk")
        self.assertEqual(user.emergency_phone, "+44 7800 000 001")
        """

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            email="boss@project.com", username="simon", password="testpass123"
        )

        self.assertEqual(user.username, "simon")
        self.assertEqual(user.email, "boss@project.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class SignupTests(TestCase):
    username = "newuser"
    email = "newuser@address.com"

    def setUp(self):
        url = reverse("account_signup")
        self.response = self.client.get(url, follow=True)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed("account/signup.html")
        self.assertTemplateNotUsed("account/login.html")
        self.assertContains(self.response, "Sign up")
        self.assertNotContains(self.response, "some nonsense not on the page")


class UserAccessTests(ModelTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.user2 = get_user_model().objects.create_user(
            email="senior@project.com",
            username="senior",
            password="testpass123",
            first_name="Senior",
        )

    def test_access_user_profile_detail_user_uuid(self):
        self.client.force_login(self.user)

        url = reverse("profile_detail", kwargs={"uuid": self.user.uuid})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, "Should be 200 Status OK response")

    def test_access_user_profile_personal_details_update_user_uuid(self):
        self.client.force_login(self.user)

        url = reverse("profile_personal_detail_update", kwargs={"uuid": self.user.uuid})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, "Should be 200 Status OK response")

    def test_access_user_profile_address_details_update_user_uuid(self):
        self.client.force_login(self.user)

        url = reverse("profile_address_detail_update", kwargs={"uuid": self.user.uuid})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200, "Should be 200 Status OK response")

    def test_access_user_profile_detail_different_user_uuid(self):
        self.client.force_login(self.user)

        url = reverse("profile_detail", kwargs={"uuid": self.user2.uuid})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 403, "Should be 403 Forbidden response")

    def test_access_user_profile_personal_details_update_different_user_uuid(self):
        self.client.force_login(self.user)

        url = reverse(
            "profile_personal_detail_update", kwargs={"uuid": self.user2.uuid}
        )
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 403, "Should be 403 Forbidden response")

    def test_access_user_profile_address_details_update_different_user_uuid(self):
        self.client.force_login(self.user)

        url = reverse("profile_address_detail_update", kwargs={"uuid": self.user2.uuid})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 403, "Should be 403 Forbidden response")
