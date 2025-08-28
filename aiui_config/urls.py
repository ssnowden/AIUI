"""AIUI URL Configuration

The `urlpatterns` list routes URLs to views.
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from environs import Env

env = Env()
env.read_env()

urlpatterns = [
    # Django admin - URL needs to be changed
    path(env("DJANGO_ADMIN"), admin.site.urls),
    # TODO: Client/user management - URL needs to be changed to use custom views in account app
    path("account/", include("allauth.urls")),
    # Project apps
    path("chats/", include("project_apps.chats.urls")),
    path("aimodels/", include("project_apps.aimodels.urls")),
    path("mm/", include("project_apps.chats.api.urls")),
    # Standard apps
    path("", include("standard.apps.hb_basicpages.urls")),
    path("account/", include("standard.apps.accounts.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("patternlibrary/", include("standard.apps.hb_pattern_libraries.urls")),
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
