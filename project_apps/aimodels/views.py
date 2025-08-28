"""project_apps.models.views.py
This module provides the views for the models app accessed by the URLs.

    Description for the views.

    --------- Base setup of views --------------
    class ModelsListView(LoginRequiredMixin, ListView):
        - Shows a list for models

    class ModelsDetailView(LoginRequiredMixin, DetailView):
        - Shows a detail view for model

    ---------- Edit views -------------
    class ModelsCreateView(LoginRequiredMixin, CreateView):
        - Create view for model

    class ModelsUpdateView(LoginRequiredMixin, UpdateView):
        - Update view for model

    class ModelsDeleteView(LoginRequiredMixin, DeleteView):
        - Delete view for model
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

import logging

from standard.views.mixins import ProjectNameMixin

from .forms import AIModelForm
from .models import AIModel

logger = logging.getLogger(__name__)


class AIModelViewPermissionTestMixin:

    def test_func(self) -> bool:
        """Checks if the current user has permission to access the view.

        This method returns True if the user is authenticated and passes any additional permission checks.
        It is intended to be overridden or extended for more complex permission logic.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        # This is part of the test for Anonymous users.
        if not self.request.user.id:
            return False
        try:
            return True
        except Exception:
            return False


class AIModelListView(ProjectNameMixin, LoginRequiredMixin, ListView):
    """Displays a list of all AIModel instances.

    This view requires the user to be logged in and shows all AI models in the system.
    The list is rendered using the specified template.

    """

    model = AIModel
    context_object_name: str = "aimodels"
    template_name: str = "aimodels/aimodels.html"


"""
    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        self.user_companies = user_profile.companies.all()
        invitations = []
        for user_company in self.user_companies:
            invitation_filter_results = Invitation.objects.filter(company=user_company)
            invitation_filter_results = list(invitation_filter_results)
            invitations = list(chain(invitations, invitation_filter_results))
        return invitations
"""


class AIModelDetailView(
    ProjectNameMixin,
    AIModelViewPermissionTestMixin,
    UserPassesTestMixin,
    LoginRequiredMixin,
    DetailView,
):
    """Displays detailed information for a single AIModel instance.

    This view requires the user to be logged in and to pass the permission test.
    The detail is rendered using the specified template.

    """

    model = AIModel
    context_object_name: str = "aimodel"
    template_name: str = "aimodels/aimodels_detail.html"


class AIModelCreateView(ProjectNameMixin, LoginRequiredMixin, CreateView):
    """Provides a form for creating a new AIModel instance.

    This view requires the user to be logged in and sets the created_by and modified_by fields.
    The form is rendered using the specified template.

    """

    model = AIModel
    form_class = AIModelForm
    context_object_name: str = "aimodel"
    template_name: str = "aimodels/aimodels_create.html"

    def form_valid(self, form: AIModelForm) -> object:
        """Handles valid form submission for creating an AIModel.

        Sets the created_by and modified_by fields to the current user before saving.

        Args:
            form (AIModelForm): The form instance containing the submitted data.

        Returns:
            object: The result of the parent class's form_valid method.
        """
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class AIModelUpdateView(
    ProjectNameMixin,
    AIModelViewPermissionTestMixin,
    UserPassesTestMixin,
    LoginRequiredMixin,
    UpdateView,
):
    """Provides a form for updating an existing AIModel instance.

    This view requires the user to be logged in and to pass the permission test.
    The modified_by field is updated to the current user.

    """

    model = AIModel
    form_class = AIModelForm
    context_object_name: str = "aimodel"
    template_name: str = "aimodels/aimodels_update.html"

    def form_valid(self, form: AIModelForm) -> object:
        """Handles valid form submission for updating an AIModel.

        Sets the modified_by field to the current user before saving.

        Args:
            form (AIModelForm): The form instance containing the submitted data.

        Returns:
            object: The result of the parent class's form_valid method.
        """
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class AIModelDeleteView(
    ProjectNameMixin,
    AIModelViewPermissionTestMixin,
    UserPassesTestMixin,
    LoginRequiredMixin,
    DeleteView,
):
    """Handles deletion of an AIModel instance.

    This view requires the user to be logged in and to pass the permission test.
    Upon successful deletion, the user is redirected to the AI models list.

    """

    model = AIModel
    context_object_name: str = "aimodel"
    template_name: str = "aimodels/aimodels_delete.html"
    success_url: str = reverse_lazy("aimodels")
