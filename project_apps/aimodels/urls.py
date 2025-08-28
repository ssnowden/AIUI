"""This module provides the URLs for the aimodels app.

It has the URLs:
    BASE URL: "procedures/".

    models: URL name to show a list of the AI Models model instances: BASE URL ONLY.

    models_detail: URL name to show the detail of a AI Models model instance: BASE URL + INSTANCE ID/.

    models_create: URL name to create a list of the AI Models model instance: BASE URL + create/ + INSTANCE ID/.

    models_update: URL name to update a list of the AI Models model instance: BASE URL + update/ + INSTANCE ID/.

    models_delete: URL name to delete a list of the AI Models model instance: BASE URL + delete/ + INSTANCE ID/.
"""

from django.urls import path

from .views import (
    AIModelCreateView,
    AIModelDeleteView,
    AIModelDetailView,
    AIModelListView,
    AIModelUpdateView,
)

urlpatterns = [
    path("", AIModelListView.as_view(), name="aimodels"),
    path("<uuid:pk>/", AIModelDetailView.as_view(), name="aimodel_detail"),
    path("create/", AIModelCreateView.as_view(), name="aimodel_create"),
    path("update/<uuid:pk>/", AIModelUpdateView.as_view(), name="aimodel_update"),
    path("delete/<uuid:pk>/", AIModelDeleteView.as_view(), name="aimodel_delete"),
]
