from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("demographics/", views.demographics_form, name="demographics"),
    path("recipient/", views.recipient_form, name="recipient"),
    path("donor/", views.donor_form, name="donor"),
    path("success/<int:id>/", views.submitted, name="submitted"),
    path("find/", TemplateView.as_view(template_name="find_plasma.html"), name="plasma"),
    path("", TemplateView.as_view(template_name="index.html"), name="share"),
    path("", TemplateView.as_view(template_name="index.html"), name="new_requests"),
    path("requests/plasma/", views.PlasmaRequestsList.as_view(), name="plasma_requests"),
    path("requests/donate/", views.DonationRequestsList.as_view(), name="donation_requests"),
    path("plasma_request_detail/<int:pk>/", views.PlasmaRequestDetail.as_view(), name="plasma_request_detail"),
    path("donation_request_detail/<int:pk>/", views.DonationRequestDetail.as_view(), name="donation_request_detail"),
    path("complete_donation_request/<int:pk>/", views.complete_donation_request, name="complete_donation_request"),
    path("complete_plasma_request/<int:pk>/", views.complete_plasma_request, name="complete_plasma_request"),
    path("undo_plasma_request/<int:pk>/", views.undo_plasma_request, name="undo_plasma_request"),
    path("undo_donation_request/<int:pk>/", views.undo_donation_request, name="undo_donation_request"),
    path("completed/donate/", views.CompletedDonationRequestsList.as_view(), name="completed_donation_requests"),
    path("completed/plasma/", views.CompletedPlasmaRequestsList.as_view(), name="completed_plasma_requests"),
    path("completed/plasma/<int:pk>/", views.PlasmaRequestDetail.as_view(), name="completed_plasma_detail"),
    path("completed/donate/<int:pk>/", views.DonationRequestDetail.as_view(), name="completed_donation_detail"),
    path("profile/", views.profile_page, name="profile"),
    path("profile/edit/", views.profile_edit, name="edit_profile"),

]


