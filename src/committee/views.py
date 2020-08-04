from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, Http404
from committee.models import Committee
from committee.forms import UpdateCommitteeForm
from account.models import Account
from event.models import EventPost
from datetime import date, timedelta

EVENT_POST_PER_PAGE = 6
today = date.today()
yesterday = today - timedelta(days=1)


def is_valid_queryparam(param):
    return param != "" and param is not None


def detail_committee_view(request, slug):
    context = {}

    committee = get_object_or_404(Committee, slug=slug)
    context["committee"] = committee

    qs = EventPost.objects.filter(author=committee.author)

    sortasc = 0

    category_query = request.GET.get("category")
    date_query = request.GET.get("date")
    price = request.GET.get("price")

    if is_valid_queryparam(date_query) and date_query != "Choose...":
        if date_query == "LATEST":
            query = qs
        elif date_query == "OLDEST":
            query = qs.order_by("date_updated")
            sortasc = 1
        elif date_query == "TODAY":
            query = qs.filter(
                date_updated__year=today.year,
                date_updated__month=today.month,
                date_updated__day=today.day,
            )
        elif date_query == "YESTERDAY":
            query = qs.filter(
                date_updated__year=yesterday.year,
                date_updated__month=yesterday.month,
                date_updated__day=yesterday.day,
            )

    if is_valid_queryparam(category_query) and category_query != "Choose...":
        query = qs.filter(category=category_query)

    if is_valid_queryparam(price) and price != "Choose..":
        if price == "Free":
            query = qs.filter(fee=0)
        elif price == "Not-Free":
            query = qs.filter(fee__gt=0)
    else:
        qry = ""
        if request.GET:
            qry = request.GET.get("q", "")
            queryset = []
            queries = qry.split(" ")
            for q in queries:
                posts = qs.filter(
                    Q(title__contains=q) | Q(body__icontains=q)
                ).distinct()
                for post in posts:
                    queryset.append(post)
            query = list(set(queryset))
        else:
            query = qs
    if sortasc == 1:
        event_posts = sorted(query, key=attrgetter("date_updated"))
    else:
        event_posts = sorted(query, key=attrgetter("date_updated"), reverse=True)

    # Pagination
    page = request.GET.get("page", 1)
    event_posts_paginator = Paginator(event_posts, EVENT_POST_PER_PAGE)

    try:
        event_posts = event_posts_paginator.page(page)
    except PageNotAnInteger:
        event_posts = event_posts_paginator.page(EVENT_POST_PER_PAGE)
    except EmptyPage:
        event_posts = event_posts_paginator.page(event_posts_paginator.num_pages)
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
            messages.success(request, f"Update successfull!")
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
            Q(name__contains=q)
            | Q(description__icontains=q)
            | Q(author__username__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)

    # create unique set and then convert to list
    return list(set(queryset))
