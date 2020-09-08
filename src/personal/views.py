from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from blog.views import get_blog_queryset
from blog.models import BlogPost, Category
from event.views import get_event_queryset, get_premium_queryset
from event.models import EventPost, EventCategory
from committee.views import get_committee_queryset
from committee.models import Committee
from .templatetags.my_tags import days_until
from datetime import date, timedelta, datetime


BLOG_POST_PER_PAGE = 10
EVENT_POST_PER_PAGE = 10

today = date.today()
yesterday = today - timedelta(days=1)


def is_valid_queryparam(param):
    return param != "" and param is not None


def home_screen_view(request):
    context = {}

    qs = BlogPost.objects.all()
    sortasc = 0

    category_query = request.GET.get("category")
    date_query = request.GET.get("date")

    if is_valid_queryparam(date_query) and date_query != "Choose...":
        if date_query == "LATEST":
            query = qs
        elif date_query == "OLDEST":
            query = qs.order_by("date_updated")
            sortasc = 1
        elif date_query == "TODAY":
            query = qs.filter(
                date_published__year=today.year,
                date_published__month=today.month,
                date_published__day=today.day,
            )
        elif date_query == "YESTERDAY":
            query = qs.filter(
                date_published__year=yesterday.year,
                date_published__month=yesterday.month,
                date_published__day=yesterday.day,
            )

    if is_valid_queryparam(category_query) and category_query != "Choose...":
        query = qs.filter(category=category_query)

    else:
        qry = ""
        if request.GET:
            qry = request.GET.get("q", "")
            context["qry"] = str(qry)

        query = get_blog_queryset(qry)

    if sortasc == 1:
        blog_posts = sorted(query, key=attrgetter("date_updated"))
    else:
        blog_posts = sorted(query, key=attrgetter("date_updated"), reverse=True)

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
    categorys = Category.objects.all()
    context["categorys"] = categorys
    return render(request, "personal/home.html", context)


def event_home_screen_view(request):
    context = {}

    qs = EventPost.objects.all()
    sortasc = 0

    for post in qs:
        expiry = days_until(post.event_date)
        if int(expiry) < 0:
            EventPost.objects.filter(id=post.id).update(is_deleted=True)
        if int(expiry) < -3:
            EventPost.objects.filter(id=post.id).delete()

    category_query = request.GET.get("category")
    date_query = request.GET.get("date")
    reg_date = request.GET.get("reg_date")
    price = request.GET.get("price")

    """
    if is_valid_queryparam(date_query) and date_query != "Choose...":
        if date_query == "LATEST":
            query = qs
        elif date_query == "OLDEST":
            query = qs.order_by("date_updated")
            sortasc = 1
        elif date_query == "TODAY":
            query = qs.filter(
                date_published__year=today.year,
                date_published__month=today.month,
                date_published__day=today.day,
            )
        elif date_query == "YESTERDAY":
            query = qs.filter(
                date_published__year=yesterday.year,
                date_published__month=yesterday.month,
                date_published__day=yesterday.day,
            )
    """
    if is_valid_queryparam(date_query):
        dates = datetime.strptime(date_query, "%Y-%m-%d")
        query = qs.filter(
            event_date__year=dates.year,
            event_date__month=dates.month,
            event_date__day=dates.day,
        )

    if is_valid_queryparam(reg_date):
        dates = datetime.strptime(reg_date, "%Y-%m-%d")
        query = qs.filter(
            reg_to__year=dates.year, reg_to__month=dates.month, reg_to__day=dates.day,
        )

    if is_valid_queryparam(category_query) and category_query != "Choose...":
        query = qs.filter(category=category_query)

    if is_valid_queryparam(price) and price != "Choose..":
        if price == "Free":
            query = qs.filter(fee=0)
        elif price == "200":
            query = qs.filter(fee__lte=200)
        elif price == "200-500":
            query = qs.filter(fee__gte=200, fee__lte=500)
        elif price == "500-1000":
            query = qs.filter(fee__gte=500, fee__lte=1000)
        elif price == "1000":
            query = qs.filter(fee__gte=100)

    else:
        qry = ""
        if request.GET:
            qry = request.GET.get("q", "")
            context["qry"] = str(qry)

        query = get_event_queryset(qry)

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
    categorys = EventCategory.objects.all()
    context["categorys"] = categorys

    return render(request, "personal/event_home.html", context)


def premium_event_screen_view(request):
    context = {}

    qs = EventPost.objects.filter(priority__gte=1)

    category_query = request.GET.get("category")
    price = request.GET.get("price")

    if is_valid_queryparam(category_query) and category_query != "Choose...":
        query = qs.filter(category=category_query).exclude(priority=0)

    if is_valid_queryparam(price) and price != "Choose..":
        if price == "Free":
            query = qs.filter(fee=0).exclude(priority=0)
        elif price == "Not-Free":
            query = qs.filter(fee__gt=0).exclude(priority=0)
    else:
        qry = ""
        if request.GET:
            qry = request.GET.get("q", "")
            context["qry"] = str(qry)

        query = get_premium_queryset(qry)

    event_posts = sorted(query, key=attrgetter("priority"), reverse=True)

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
    categorys = EventCategory.objects.all()
    context["categorys"] = categorys

    return render(request, "personal/premium_events.html", context)


def committee_home_screen_view(request):
    context = {}

    qry = ""
    if request.GET:
        qry = request.GET.get("q", "")
        context["qry"] = str(qry)

    query = get_committee_queryset(qry)

    committee = sorted(query, key=attrgetter("date_updated"), reverse=True)
    context["committee"] = committee
    return render(request, "personal/committee_home.html", context)
