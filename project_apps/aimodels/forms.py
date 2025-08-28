"""project_apps.models.forms.py

Description for the form.

class AIModelForm(forms.ModelForm)
    - base model form.
    - fields:
        - name
        - description
        - access_mode
        - access_endpoint
        - token_cost_per_1M_input
        - token_cost_per_1M_output
        - best_use_cases
        - max_tokens
        - is_active
    - widgets:
        "name": forms.TextInput(
        "description": forms.Textarea(
        "access_mode": forms.Select(
        "access_endpoint": forms.URLInput(
        "token_cost_per_1M_input": forms.NumberInput(
        "token_cost_per_1M_output": forms.NumberInput(
        "best_use_cases": forms.Textarea(
        "max_tokens": forms.NumberInput(
        "is_active": forms.CheckboxInput(

    - error messages:

"""

import logging

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import AIModel

logger = logging.getLogger(__name__)


class AIModelForm(forms.ModelForm):
    """
    A model form for creating and editing AIModel instances.
    This form customizes widgets and field attributes for better user experience in the admin or custom UIs.
    """

    class Meta:
        model: type = AIModel
        fields: tuple[str, ...] = (
            "name",
            "description",
            "access_mode",
            "access_endpoint",
            "token_cost_per_1M_input",
            "token_cost_per_1M_output",
            "best_use_cases",
            "max_tokens",
            "is_active",
        )

        widgets: dict[str, forms.Widget] = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": _(
                        "What is the name for the model? This should be the formal name used by the model provider (e.g. deepseek/deepseek-r1-0528:free)"
                    ),
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": _("What is the description for the model?"),
                }
            ),
            "access_mode": forms.Select(
                attrs={
                    "class": "form-select form-select-md text-white",
                }
            ),
            "access_endpoint": forms.URLInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": _(
                        "The access endpoint for the model (e.g. https://openrouter.ai/api/v1)"
                    ),
                }
            ),
            "token_cost_per_1M_input": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": _("The cost of 1 million tokens for input"),
                }
            ),
            "token_cost_per_1M_output": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": _("The cost of 1 million tokens for output"),
                }
            ),
            "best_use_cases": forms.Textarea(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": _("What are the best use cases for the model?"),
                }
            ),
            "max_tokens": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-lg",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }
