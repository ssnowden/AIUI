from django.urls import path

from .views import AboutPageView, HomePageView, TnCsPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("tncs/", TnCsPageView.as_view(), name="tncs"),
]
