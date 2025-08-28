from django.urls import path

from .views import NOAMultiModalEndpoint

urlpatterns = [
    path("mm/", NOAMultiModalEndpoint.as_view(), name="noa-mm-endpoint"),
]
