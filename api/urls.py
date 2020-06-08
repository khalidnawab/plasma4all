from django.urls import include, path
from . import views

urlpatterns = [
    path('getplasmarequests', views.get_plasma_requests),
    path('getdonationrequests', views.get_donation_requests),
    #path('addplasmarequest', views.add_plasma_request),
    #path('adddonationrequest', views.add_donation_request),
]