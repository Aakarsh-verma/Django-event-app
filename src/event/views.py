from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from event.models import EventPost
from event.forms import CreateEventPostForm, UpdateEventPostForm
from account.models import Account


@login_required
def create_event_view(request):

    context = {}

    user = request.user

    if user.is_staff == 1 or user.is_superuser == 1:
        form = CreateEventPostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            author = Account.objects.filter(email=user.email).first()
            obj.author = author
            obj.save()
            messages.success(request, f"Your Blog has been posted!")
            form = CreateEventPostForm()

        context["form"] = form
        return render(request, "event/create_event.html", {})
    else:
        raise Http404("Page Not Found")


def detail_event_view(request, slug):
    context = {}

    event_post = get_object_or_404(EventPost, slug=slug)
    context["event_post"] = event_post

    return render(request, "event/detail_event.html", context)


@login_required
def edit_event_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")

    event_post = get_object_or_404(EventPost, slug=slug)

    if event_post.author != user:
        return HttpResponse("You are not the author of that post.")

    if request.POST:
        form = UpdateEventPostForm(
            request.POST or None, request.FILES or None, instance=event_post
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context["success_message"] = "Updated"
            event_post = obj

    form = UpdateEventPostForm(
        initial={
            "title": event_post.title,
            "body": event_post.body,
            "image": event_post.image,
            "category": event_post.category,
            "event_date": event_post.event_date,
            "reg_to": event_post.reg_to,
            "fee": event_post.fee,
            "reg_link": event_post.reg_link,
        }
    )

    context["form"] = form
    return render(request, "event/edit_event.html", context)


def get_event_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = EventPost.objects.filter(
            Q(title__contains=q) | Q(body__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)

    # create unique set and then convert to list
    return list(set(queryset))
