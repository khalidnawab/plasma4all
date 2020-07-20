from django.core.validators import RegexValidator
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
    (6, "Azad Kashmir"),
    (7, "Gilgit Baltistan"),
    (8, "FATA"),
)

BLOOD = (
    (0, "A+"),
    (1, "A-"),
    (2, "B+"),
    (3, "B-"),
    (4, "O+"),
    (5, "O-"),
    (6, "AB+"),
    (7, "AB-"),
    (8, "Unknown"),
)
# Create your models here.


class Profile(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30)
    province = models.IntegerField(choices=PROVINCES, default=4)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.IntegerField(choices=GENDER, default=3)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    date_covid_19_diagnosed = models.DateField(null=True, blank=True)
    blood_group = models.IntegerField(choices=BLOOD, default=8)
    hospital_which_labelled_positive = models.CharField(max_length=30, blank=True)
    hospital_which_labelled_negative = models.CharField(max_length=30, blank=True)
    lab_which_labelled_positive = models.CharField(max_length=30, blank=True)
    lab_which_labelled_negative = models.CharField(max_length=30, blank=True)
    donation_request = models.BooleanField(default=False)
    plasma_request = models.BooleanField(default=False)
    donation_completed = models.BooleanField(default=False)
    plasma_completed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
