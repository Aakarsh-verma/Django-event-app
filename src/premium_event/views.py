from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from premium_event.models import PremiumEventPost
from premium_event.forms import CreatePremiumEventPostForm, UpdatePremiumEventPostForm
from account.models import Account


@login_required
def create_premium_event_view(request):

    context = {}

    user = request.user
    if user.is_staff == 1 or user.is_superuser == 1:
        if request.POST:
            form = CreatePremiumEventPostForm(
                request.POST or None, request.FILES or None
            )
            if form.is_valid():
                obj = form.save(commit=False)
                author = Account.objects.filter(email=user.email).first()
                obj.author = author
                obj.save()
                messages.success(
                    request, f"Your PremiumEvent has been posted successfully!"
                )
                return redirect("premium_event-home")
            else:
                context["form"] = form
        else:
            form = CreatePremiumEventPostForm()
            context["form"] = form
        return render(request, "premium_event/create_premium_event.html", context)

    else:
        raise Http404("Page Not Found")


def detail_premium_event_view(request, slug):
    context = {}

    premium_event_post = get_object_or_404(PremiumEventPost, slug=slug)
    context["premium_event_post"] = premium_event_post

    return render(request, "premium_event/detail_premium_event.html", context)


@login_required
def edit_premium_event_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")

    premium_event_post = get_object_or_404(PremiumEventPost, slug=slug)

    if premium_event_post.author != user:
        return HttpResponse("You are not the author of that post.")

    if request.POST:
        form = UpdatePremiumEventPostForm(
            request.POST or None, request.FILES or None, instance=premium_event_post
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(
                request, f"Your PremiumEvent has been updated successfully!"
            )
            premium_event_post = obj
            return redirect("premium_event-home")

    form = UpdatePremiumEventPostForm(
        initial={
            "title": premium_event_post.title,
            "body": premium_event_post.body,
            "image": premium_event_post.image,
            "category": premium_event_post.category,
            "premium_event_date": premium_event_post.premium_event_date,
            "reg_to": premium_event_post.reg_to,
            "fee": premium_event_post.fee,
            "reg_link": premium_event_post.reg_link,
        }
    )

    context["form"] = form
    return render(request, "premium_event/edit_premium_event.html", context)


@login_required
def delete_premium_event_view(request, id):

    context = {}
    premium_event_post = get_object_or_404(PremiumEventPost, id=id)
    if request.method == "POST":
        premium_event_post.delete()
        messages.success(request, f"Your PremiumEvent has been deleted successfully!")
        return redirect("premium_event-home")

    context["premium_event_post"] = premium_event_post
    return render(request, "premium_event/delete_premium_event.html", context)


def get_premium_event_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = PremiumEventPost.objects.filter(
            Q(title__contains=q)
            | Q(body__icontains=q)
            | Q(author__username__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)

    # create unique set and then convert to list
    return list(set(queryset))
