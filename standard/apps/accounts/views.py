from allauth.account.views import LoginView, PasswordChangeView, SignupView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    AccessMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from standard.views.mixins import ProjectNameMixin

from .forms import (
    CustomUserAddressDetailsUpdateForm,
    CustomUserPersonalDetailsUpdateForm,
)

UserModel = get_user_model()


class ProfilePageView(
    ProjectNameMixin,
    UserPassesTestMixin,
    LoginRequiredMixin,
    generic.DetailView,
):
    model = UserModel
    template_name = "account/profile_detail.html"
    pk_url_kwarg = "uuid"
    queryset = UserModel.objects.all()
    login_url = reverse_lazy("account_login")

    def get_object(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(UserModel, uuid=id)

    def test_func(self):
        if hasattr(self.request.user, "uuid"):
            return self.request.user.uuid == self.kwargs.get(self.pk_url_kwarg)
        else:
            return False


class ProfileEditPersonalDetailsPageView(
    ProjectNameMixin,
    UserPassesTestMixin,
    LoginRequiredMixin,
    generic.UpdateView,
):
    model = UserModel
    form_class = CustomUserPersonalDetailsUpdateForm
    template_name = "account/profile_personal_detail_update.html"
    pk_url_kwarg = "uuid"
    queryset = UserModel.objects.all()
    login_url = reverse_lazy("account_login")

    def get_object(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(UserModel, uuid=id)

    def test_func(self):
        if hasattr(self.request.user, "uuid"):
            return self.request.user.uuid == self.kwargs.get(self.pk_url_kwarg)
        else:
            return False


class ProfileEditAddressDetailsPageView(
    UserPassesTestMixin,
    LoginRequiredMixin,
    generic.UpdateView,
):
    model = UserModel
    form_class = CustomUserAddressDetailsUpdateForm
    template_name = "account/profile_address_detail_update.html"
    pk_url_kwarg = "uuid"
    queryset = UserModel.objects.all()
    login_url = reverse_lazy("account_login")

    def get_object(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(UserModel, uuid=id)

    def test_func(self):
        if hasattr(self.request.user, "uuid"):
            return self.request.user.uuid == self.kwargs.get(self.pk_url_kwarg)
        else:
            return False


""" Any other profile style pages e.g. 
class ProfileEditEmergencyContactPageView(
    UserPassesTestMixin,
    LoginRequiredMixin,
    generic.UpdateView,
):
    model = UserModel
    form_class = CustomUserEmergencyContactUpdateForm
    template_name = "account/profile_emergency_contact_update.html"
    pk_url_kwarg = "uuid"
    queryset = UserModel.objects.all()
    login_url = reverse_lazy("account_login")

    def get_object(self):
        id = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(UserModel, uuid=id)

    def test_func(self):
        if hasattr(self.request.user, "uuid"):
            return self.request.user.uuid == self.kwargs.get(self.pk_url_kwarg)
        else:
            return False
"""


class CustomPasswordChangeView(
    ProjectNameMixin, LoginRequiredMixin, PasswordChangeView
):
    success_url = reverse_lazy("home")


class LoginView(ProjectNameMixin, LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy("home")


class SignupView(ProjectNameMixin, LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy("home")
