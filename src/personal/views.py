from django.shortcuts import render
from operator import attrgetter
from django.db.models import Q, Count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from blog.views import get_blog_queryset
from blog.models import BlogPost
from event.views import get_event_queryset
from event.models import EventPost
from committee.views import get_committee_queryset
from committee.models import Committee


BLOG_POST_PER_PAGE = 6


def home_screen_view(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get("q", "")
        context["query"] = str(query)

    blog_posts = sorted(
        get_blog_queryset(query), key=attrgetter("date_updated"), reverse=True
    )

    # Pagination
    page = request.GET.get("page", 1)
    blog_posts_paginator = Paginator(blog_posts, BLOG_POST_PER_PAGE)

    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POST_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    context["blog_posts"] = blog_posts

    return render(request, "personal/home.html", context)


EVENT_POST_PER_PAGE = 6


def event_home_screen_view(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get("q", "")
        context["query"] = str(query)

    event_posts = sorted(
        get_event_queryset(query), key=attrgetter("date_updated"), reverse=True
    )

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

    return render(request, "personal/event_home.html", context)


def committee_home_screen_view(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get("q", "")
        context["query"] = str(query)

    committee = sorted(
        get_committee_queryset(query), key=attrgetter("date_updated"), reverse=True
    )
    context["committee"] = committee
    return render(request, "personal/committee_home.html", context)


def is_valid_queryparam(param):
    return param != "" and param is not None

