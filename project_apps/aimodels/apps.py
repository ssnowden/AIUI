"""This module defines the app configuration.

It has the Config class:
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ModelsConfig(AppConfig):
    name: str = "project_apps.aimodels"
    verbose_name: str = _("AI Models")
