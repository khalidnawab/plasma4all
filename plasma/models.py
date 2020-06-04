from django.db import models
from django.contrib.auth.models import User

GENDER = (
    (0, "Male"),
    (1, "Female"),
    (2, "Other"),
    (3, "Unspecified"),
)

PROVINCES = (
    (0, "Khyber Pakhtunkhwah"),
    (1, "Punjab"),
    (2, "Sindh"),
    (3, "Balochistan"),
    (4, "Unspecified"),
    (5, "Islamabad Capital Territory"),
    (6, "Azad Kashmir")
)


# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    province = models.IntegerField(choices=PROVINCES, default=4)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.IntegerField(choices=GENDER, default=3)
    phone = models.IntegerField(default=0)
    date_COVID_19_diagnosed = models.DateField(null=True, blank=True)
    hospital_which_labelled_positive = models.CharField(max_length=30, blank=True)
    hospital_which_labelled_negative = models.CharField(max_length=30, blank=True)
    lab_which_labelled_positive = models.CharField(max_length=30, blank=True)
    lab_which_labelled_negative = models.CharField(max_length=30, blank=True)
    donation_request = models.BooleanField(default=False)
    plasma_request = models.BooleanField(default=False)
    donation_completed = models.BooleanField(default=False)
    plasma_completed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
