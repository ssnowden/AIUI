""" This module defines the app configuration.

It has the Config class:
"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ChatsConfig(AppConfig):
    name = "project_apps.chats"
    verbose_name = _("Chats")
