from django.urls import path

from .views import (
    ProfilePageView,
    ProfileEditPersonalDetailsPageView,
    ProfileEditAddressDetailsPageView,
    CustomPasswordChangeView,
)

""" Any other pages that views that are required e.g. 
    ProfileEditEmergencyContactPageView,
"""
urlpatterns = [
    path("detail/<uuid:uuid>/", ProfilePageView.as_view(), name="profile_detail"),
    path(
        "personaldetailupdate/<uuid:uuid>/",
        ProfileEditPersonalDetailsPageView.as_view(),
        name="profile_personal_detail_update",
    ),
    path(
        "addressdetailupdate/<uuid:uuid>/",
        ProfileEditAddressDetailsPageView.as_view(),
        name="profile_address_detail_update",
    ),
    path(
        "passwordchange/",
        CustomPasswordChangeView.as_view(),
        name="custom_password_change",
    ),
]
""" Any other pages as appropriate e.g.
path(
    "emergencycontactupdate/<uuid:uuid>/",
    ProfileEditEmergencyContactPageView.as_view(),
    name="profile_emergency_contact_update",
),
"""
