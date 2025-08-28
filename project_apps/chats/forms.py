"""project_apps.chats.forms.py

Description for the forms.

--------- Base setup of forms and formset --------------
class ConversationThreadForm(forms.ModelForm)
    - base model form.
    - fields: ("name", "aimodel")
    - widgets: ("name", "aimodel")
    - error messages:

class ConversationItemForm(forms.ModelForm)
    - item model form.
    - fields: ("conversation_thread", "prompt", "ORDER")
    - widgets: ("conversation_thread", "prompt", "ORDER")
    - error messages: ("prompt")

class ConversationItemFormSet(BaseInlineFormSet):
    - Base formset for ConversationItem within ConversationThread.
    - add_fields: override to ensure all forms are validated.
    - clean: (commented out) example of custom validation logic.

ConversationItemFormset = inlineformset_factory(...)
    - Base formset factory definition.

"""

import logging

from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory
from django.utils.translation import gettext_lazy as _

from .models import ConversationItem, ConversationThread

logger = logging.getLogger(__name__)


class ConversationThreadForm(forms.ModelForm):
    """Form for creating and editing ConversationThread instances.

    This form allows users to input the name and AI model for a chat conversation thread.
    It uses custom widgets for improved user experience.

    Attributes:
        Meta: Configuration for the form, including model, fields, and widgets.
    """

    class Meta:
        model: type = ConversationThread
        fields: tuple[str, ...] = ("name", "aimodel")

        widgets: dict[str, forms.Widget] = {
            "name": forms.fields.TextInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": _("Name for the chat"),
                }
            ),
            "aimodel": forms.Select(
                attrs={
                    "class": "form-select form-select-md text-white",
                }
            ),
        }


class ConversationItemForm(forms.ModelForm):
    """Form for creating and editing ConversationItem instances.

    This form is used to add or update items (prompts) within a conversation thread.
    It enforces that the prompt field is required and customizes widgets and error messages.

    Attributes:
        Meta: Configuration for the form, including model, fields, widgets, and error messages.
    """

    class Meta:
        model: type = ConversationItem
        fields: tuple[str, ...] = ("conversation_thread", "prompt", "ORDER")

        widgets: dict[str, forms.Widget] = {
            "conversation_thread": forms.HiddenInput(),
            "prompt": forms.Textarea(
                attrs={
                    "class": "form-control form-control-lg",
                    "placeholder": _("What do you want to do?"),
                    "rows": 3,
                }
            ),
            "ORDER": forms.HiddenInput(),
        }

        error_messages: dict[str, dict[str, str]] = {
            "prompt": {
                "required": _("required. A prompt must be posted."),
            },
        }

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Initializes the ConversationItemForm and sets the prompt field as required.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.fields["prompt"].required = True

    def save(self, commit: bool = ...) -> ConversationItem:
        """Saves the ConversationItem instance, setting a default token value.

        Args:
            commit: Whether to commit the save to the database.

        Returns:
            ConversationItem: The saved ConversationItem instance.
        """
        # TODO: This is a default and actually needs to be calculated
        self.instance.tokens = 2
        return super().save(commit)


class ConversationItemFormSet(BaseInlineFormSet):
    """Formset for managing multiple ConversationItem forms within a thread.

    This formset ensures that all forms are validated and can be extended with custom validation logic.
    """

    def add_fields(self, form: forms.Form, index: int) -> None:
        """Adds fields to each form in the formset and ensures validation.

        Args:
            form: The form instance to add fields to.
            index: The index of the form in the formset.
        """

        super().add_fields(form, index)
        form.empty_permitted = False  # This ensures all forms are validated

    # def clean(self) -> None:
    #     super().clean()
    #     texts: list[str] = []
    #     for form in self.forms:
    #         if self.can_delete and self._should_delete_form(form):
    #             continue
    #         '''Validating uniqueness in a formset's model'''
    #         if form.cleaned_data:
    #             text: str = form.cleaned_data["field_name"]
    #             if text in texts:
    #                 raise ValidationError(_("Items in a list must have distinct text"))
    #             texts.append(text)


ConversationItemFormset: type = inlineformset_factory(
    parent_model=ConversationThread,
    model=ConversationItem,
    form=ConversationItemForm,
    formset=ConversationItemFormSet,
    extra=1,
    can_order=True,
)
