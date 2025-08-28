from django.urls import path
from .views import (
    PatternLibraryOverView,
    PatternLibraryCSS,
    PatternLibraryColors,
    PatternLibraryTemplates,
    PatternLibraryBtn,
    PatternLibraryDatepicker,
    PatternLibraryAlert,
    PatternLibraryBadge,
    PatternLibraryAvatar,
    PatternLibraryListGroupItem,
    PatternLibraryTable,
    PatternLibraryLink,
)

urlpatterns = [
    path("", PatternLibraryOverView.as_view(), name="patternlibrary_overview"),
    path("css/", PatternLibraryCSS.as_view(), name="patternlibrary_css"),
    path("colors/", PatternLibraryColors.as_view(), name="patternlibrary_colors"),
    path("templates/", PatternLibraryTemplates.as_view(), name="patternlibrary_templates"),
    path("alerts/", PatternLibraryAlert.as_view(), name="patternlibrary_alert"),
    path("avatar/", PatternLibraryAvatar.as_view(), name="patternlibrary_avatar"),
    path("badge/", PatternLibraryBadge.as_view(), name="patternlibrary_badge"),
    path("btn/", PatternLibraryBtn.as_view(), name="patternlibrary_button"),
    path("datepicker/", PatternLibraryDatepicker.as_view(), name="patternlibrary_datepicker"),
    path(
        "listgroupitem/",
        PatternLibraryListGroupItem.as_view(),
        name="patternlibrary_list_group_item",
    ),
    path("table/", PatternLibraryTable.as_view(), name="patternlibrary_table"),
    path("link/", PatternLibraryLink.as_view(), name="patternlibrary_link"),
]