from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from operator import attrgetter
from django.http import HttpResponse, Http404
from committee.models import Committee
from committee.forms import UpdateCommitteeForm
from account.models import Account
from event.models import EventPost


def detail_committee_view(request, slug):
    context = {}

    committee = get_object_or_404(Committee, slug=slug)
    context["committee"] = committee

    event_posts = sorted(
        EventPost.objects.filter(author=committee.author),
        key=attrgetter("date_updated"),
        reverse=True,
    )
    context["event_posts"] = event_posts

    return render(request, "committee/detail_committee.html", context)


def edit_committee_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")

    committee = get_object_or_404(Committee, slug=slug)

    if committee.author != user:
        return HttpResponse("You are not the author of that post.")

    if request.POST:
        form = UpdateCommitteeForm(
            request.POST or None, request.FILES or None, instance=committee
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context["success_message"] = "Updated"
            committee = obj

    form = UpdateCommitteeForm(
        initial={
            "name": committee.name,
            "description": committee.description,
            "link": committee.link,
            "image": committee.image,
            "back_image": committee.back_image,
        }
    )

    context["form"] = form
    return render(request, "committee/edit_committee.html", context)


def get_committee_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Committee.objects.filter(
            Q(name__contains=q) | Q(description__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)

    # create unique set and then convert to list
    return list(set(queryset))
