from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from operator import attrgetter
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from blog.models import BlogPost
from event.views import get_event_queryset
from account.models import Account
from event.models import EventPost
from datetime import datetime, date
from django.contrib.auth.decorators import login_required


def registration_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            messages.success(
                request, f"Registration successfull!You are now able to login!"
            )
            return redirect("home")
        else:
            context["form"] = form

    else:
        form = RegistrationForm()
        context["form"] = form
    return render(request, "account/register.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")


def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context["form"] = form
    return render(request, "account/login.html", context)


@login_required
def account_view(request):

    context = {}
    apply = EventPost.objects.filter(
        author=request.user, premium_applied=False, premium_aproved=False
    )
    context["apply"] = apply

    event_post = EventPost.objects.filter(author=request.user)
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST["email"],
                "username": request.POST["username"],
            }
            form.save()
            messages.success(request, f"Profile Update successfull!")
    else:
        form = AccountUpdateForm(
            initial={"email": request.user.email, "username": request.user.username,}
        )
    context["form"] = form

    # qry = ""
    # if request.GET:
    #    qry = request.GET.get("q", "")
    #    context["qry"] = str(qry)

    # query = get_event_queryset(qry)
    # event_post = sorted(query, key=attrgetter("date_updated"), reverse=True)
    context["event_post"] = event_post

    return render(request, "account/account.html", context)


def must_authenticate_view(request):
    return render(request, "account/must_authenticate.html", {})
