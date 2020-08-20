from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q
from mysite.settings import EMAIL_HOST_USER
from operator import attrgetter
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from event.models import EventPost, EventCategory
from event.forms import (
    CreateEventPostForm,
    UpdateEventPostForm,
    ApplyPremiumForm,
    ApprovePremiumForm,
)
from account.models import Account
from blog.models import BlogPost


@login_required
def create_event_view(request):

    context = {}
    categorys = EventCategory.objects.all()

    user = request.user
    if user.is_staff == 1 or user.is_superuser == 1:
        if request.POST:
            form = CreateEventPostForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                obj = form.save(commit=False)
                author = Account.objects.filter(email=user.email).first()
                obj.author = author
                obj.save()

                messages.success(request, f"Your Event has been posted successfully!")
                return redirect("event-home")
            else:
                print(form)
                print("Invalid Form")
                print(form.errors)
                return render(request, "event/create_event.html", {"form": form})
        else:
            form = CreateEventPostForm()
            context["form"] = form
            context["categorys"] = categorys
        return render(request, "event/create_event.html", context)

    else:
        raise Http404("Page Not Found")


def detail_event_view(request, slug):
    context = {}

    blog_posts = BlogPost.objects.all()
    blog_posts = sorted(blog_posts, key=attrgetter("date_updated"), reverse=True)
    context["blog_posts"] = blog_posts

    event_post = get_object_or_404(EventPost, slug=slug)
    context["event_post"] = event_post

    return render(request, "event/detail_event.html", context)


@login_required
def edit_event_view(request, slug):
    context = {}
    categorys = EventCategory.objects.all()

    user = request.user
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
            messages.success(request, f"Your Event has been updated successfully!")
            event_post = obj
            return redirect("event-home")

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
    context["categorys"] = categorys
    context["event_post"] = event_post
    return render(request, "event/edit_event.html", context)


@login_required
def delete_event_view(request, id):

    context = {}
    event_post = get_object_or_404(EventPost, id=id)
    if request.method == "POST":
        event_post.delete()
        messages.success(request, f"Your Event has been deleted successfully!")
        return redirect("event-home")

    context["event_post"] = event_post
    return render(request, "event/delete_event.html", context)


@login_required
def apply_premium_view(request):
    context = {}
    user = request.user
    event_post = EventPost.objects.filter(
        author=request.user, premium_applied=False, premium_aproved=False
    )
    context["event_post"] = event_post
    return render(request, "event/apply_premium.html", context)


@login_required
def confirm_apply_view(request, slug):
    context = {}
    user = request.user

    event_post = get_object_or_404(EventPost, slug=slug)
    if event_post.author != user:
        return HttpResponse("You are not the author of that post.")

    subject = "Submission of Application for Premium Event"
    html_message = render_to_string(
        "event/premium_applied.html", {"event_post": "event_post"}
    )
    plain_message = strip_tags(html_message)
    from_email = str(EMAIL_HOST_USER)
    emailto = [
        str(user.email),
    ]
    # email = EmailMessage(subject, plain_message, from_email, emailto)
    # email.content_subtype = "html"

    subject2 = "Submission of Application for Premium Event"
    html_message2 = render_to_string(
        "event/premium_applied2.html", {"event_post": "event_post"}
    )
    plain_message2 = strip_tags(html_message2)
    from_email2 = str(EMAIL_HOST_USER)
    emailto2 = [
        str(EMAIL_HOST_USER),
    ]
    # email2 = EmailMessage(subject2, plain_message2, from_email2, emailto2)
    # email2.content_subtype = "html"

    if request.POST:
        form = ApplyPremiumForm(
            request.POST or None, request.FILES or None, instance=event_post
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(
                request, f"Your Event has been Applied For premium successfully!"
            )
            event_post = obj
            send_mail(
                subject, plain_message, from_email, emailto, html_message=html_message
            )
            send_mail(
                subject2,
                plain_message2,
                from_email2,
                emailto2,
                html_message=html_message2,
            )
            return redirect("event-home")

    form = ApplyPremiumForm(initial={"premium_applied": event_post.premium_applied,})

    context["form"] = form
    context["event_post"] = event_post
    return render(request, "event/confirm_apply.html", context)


@login_required
def approve_premium_view(request):
    context = {}
    event_post = EventPost.objects.filter(premium_applied=True, premium_aproved=False)
    context["event_post"] = event_post
    return render(request, "event/approve_premium.html", context)


@login_required
def confirm_premium_view(request, slug):
    context = {}
    user = request.user

    if user.is_superuser:
        event_post = get_object_or_404(EventPost, slug=slug)

        subject = "Premium Event is Live!"
        html_message = render_to_string(
            "event/premium_approved.html", {"event_post": "event_post"}
        )
        plain_message = strip_tags(html_message)
        from_email = str(EMAIL_HOST_USER)
        emailto = [
            str(event_post.author.email),
        ]

        if request.POST:
            form = ApprovePremiumForm(
                request.POST or None, request.FILES or None, instance=event_post
            )
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                messages.success(
                    request, f"The Event has been successfully swicthed to Premium!"
                )
                event_post = obj
                send_mail(
                    subject,
                    plain_message,
                    from_email,
                    emailto,
                    html_message=html_message,
                )
                return redirect("event-home")

        form = ApprovePremiumForm(
            initial={"premium_aproved": event_post.premium_aproved,}
        )

        context["form"] = form
        context["event_post"] = event_post
        return render(request, "event/confirm_premium.html", context)
    else:
        raise Http404("Not Found")


def get_event_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = EventPost.objects.filter(
            Q(title__contains=q)
            | Q(body__icontains=q)
            | Q(author__username__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)

    # create unique set and then convert to list
    return list(set(queryset))


def get_premium_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = (
            EventPost.objects.filter(
                Q(title__contains=q)
                | Q(body__icontains=q)
                | Q(author__username__icontains=q)
            )
            .distinct()
            .exclude(priority=0)
        )
        for post in posts:
            queryset.append(post)

    # create unique set and then convert to list
    return list(set(queryset))
