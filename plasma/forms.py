from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class DateInput(forms.DateInput):
    input_type = 'date'


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="(Optional)")
    last_name = forms.CharField(max_length=30, required=False, help_text="(Optional)")
    email = forms.EmailField(
        max_length=254, help_text="Please provide a valid email address."
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class DemographicsForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["author", "user", "plasma_request", "plasma_completed", "donation_request", "donation_completed"]


class DonorForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["author", "plasma_request", "plasma_completed", "donation_request", "donation_completed"]
        widgets = {
            'birth_date': DateInput(),
            'date_covid_19_diagnosed': DateInput(),
        }


class RecipentForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["author", "plasma_request", "plasma_completed", "donation_request", "donation_completed",
                   "hospital_which_labelled_negative", "lab_which_labelled_negative"]
        widgets = {
            'birth_date': DateInput(),
            'date_covid_19_diagnosed': DateInput(),
        }
