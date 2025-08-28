"""
ASGI config for AIUI project found in aiui_config.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aiui_config.settings")

application = get_asgi_application()
