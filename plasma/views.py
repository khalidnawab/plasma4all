from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Profile
from django.core.mail import send_mail
from django.views import generic
from plasma4me.settings import ADMIN_EMAIL
from django.contrib import messages

# Create your views here.
from plasma.forms import SignUpForm, DemographicsForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("demographics")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


@login_required(login_url="/")
def profile_page(request):
    # load data from the user table
    profile = User.objects.get(username=request.user)
    # we will check if the demographics on the user exist in the Profile table. If there is no data,
    # a page displaying a form for user demographics is rendered, otherwise the page dispalying
    # user data is displayed.
    try:
        demographics = Profile.objects.get(user=request.user)
    except:
        if request.method == "POST":
            form = DemographicsForm(request.POST)
            if form.is_valid():
                new_profile = form.save(commit=False)
                new_profile.user = request.user
                new_profile.save()
                return redirect("profile")
        else:
            form = DemographicsForm()
        return render(request, "general_form.html", {"form": form})

    return render(
        request, "profile.html", {"profile": profile, "demographics": demographics}
    )


@login_required(login_url="/")
def demographics_form(request):
    if request.method == "POST":
        form = DemographicsForm(request.POST)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            return redirect("home")
    else:
        form = DemographicsForm
    return render(request, "demographics_form.html", {"form": form})


@login_required(login_url="/")
def submitted(request, id):
    if Profile.objects.filter(user=request.user).exists():
        user = Profile.objects.get(user=request.user)
        if id == 2 and not user.donation_request:
            user.donation_request = True
            user.save()
            user_request = "donation"
        elif id == 1 and not user.plasma_request:
            user.plasma_request = True
            user.save()
            user_request = "Plasma"
        else:
            messages.warning(request, 'You have already submitted a request, our team will contact you soon. Thank you for your patience.')
            return redirect("home")
        send_mail(
            'New Request for {}'.format(user_request),
            'You have a new request for {}'.format(user_request),
            'from@example.com',
            [ADMIN_EMAIL],
            fail_silently=False,
        )
        return render(request, "request.html")
    else:
        messages.warning(request, 'You need to fill this form before you can submit a request.')
        return redirect('profile')


class DonationRequestsList(LoginRequiredMixin, generic.ListView):
    model = Profile
    template_name = "donation_request_list.html"

    # notes to be arranged based on date they were created using the following method.
    def get_queryset(self):
        return (
            Profile.objects.filter(donation_request=1, donation_completed=0)
                .order_by("-created_on")
        )


class PlasmaRequestsList(LoginRequiredMixin, generic.ListView):
    model = Profile
    template_name = "plasma_request_list.html"

    # notes to be arranged based on date they were created using the following method.
    def get_queryset(self):
        return (
            Profile.objects.filter(plasma_request=1, plasma_completed=0)
                .order_by("-created_on")
        )


"""using generic detailview to render the page to display details of the note item."""


class PlasmaRequestDetail(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = "plasma_request_detail.html"


class DonationRequestDetail(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = "donation_request_detail.html"


@login_required(login_url="/")
def complete_plasma_request(request, pk):
    user = Profile.objects.get(pk=pk)
    user.plasma_completed = 1
    user.save()
    return redirect("plasma_requests")


@login_required(login_url="/")
def complete_donation_request(request, pk):
    user = Profile.objects.get(pk=pk)
    user.donation_completed = 1
    user.save()
    return redirect("donation_requests")


@login_required(login_url="/")
def undo_plasma_request(request, pk):
    user = Profile.objects.get(pk=pk)
    user.plasma_completed = 0
    user.save()
    return redirect("plasma_requests")


@login_required(login_url="/")
def undo_donation_request(request, pk):
    user = Profile.objects.get(pk=pk)
    user.donation_completed = 0
    user.save()
    return redirect("donation_requests")


class CompletedDonationRequestsList(LoginRequiredMixin, generic.ListView):
    model = Profile
    template_name = "completed_donation_list.html"

    # notes to be arranged based on date they were created using the following method.
    def get_queryset(self):
        return (
            Profile.objects.filter(donation_completed=1)
                .order_by("-created_on")
        )


class CompletedPlasmaRequestsList(LoginRequiredMixin, generic.ListView):
    model = Profile
    template_name = "completed_plasma_list.html"

    # notes to be arranged based on date they were created using the following method.
    def get_queryset(self):
        return (
            Profile.objects.filter(plasma_completed=1)
                .order_by("-created_on")
        )


@login_required(login_url="/")
def profile_page(request):
    # load data from the user table
    user = User.objects.get(username=request.user)
    # we will check if the demographics on the user exist in the Profile table. If there is no data,
    # a page displaying a form for user demographics is rendered, otherwise the page dispalying
    # user data is displayed.
    try:
        demographics = Profile.objects.get(user=request.user)
    except:
        if request.method == "POST":
            form = DemographicsForm(request.POST)
            if form.is_valid():
                new_profile = form.save(commit=False)
                new_profile.user = request.user
                new_profile.save()
                return redirect("profile")
        else:
            form = DemographicsForm()
        return render(request, "general_form.html", {"form": form})

    return render(
        request, "profile.html", {"user": user, "demographics": demographics}
    )


@login_required(login_url="/")
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    form = DemographicsForm(instance=profile)

    if request.method == "POST":
        form = DemographicsForm(request.POST, instance=profile)
        if form.is_valid():
            profile.save()
            return redirect("profile")
    else:

        return render(request, "general_form.html", {"form": form})
