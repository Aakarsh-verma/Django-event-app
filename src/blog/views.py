from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, Http404
from account.models import Account
from event.models import EventPost
from blog.models import BlogPost, Category
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm


@login_required
def create_blog_view(request):

    context = {}
    categorys = Category.objects.all()
    context["categorys"] = categorys

    user = request.user
    event_posts = EventPost.objects.filter(author=user)
    context["event_posts"] = event_posts

    if user.is_staff == 1 or user.is_faculty == 1:
        if request.POST:
            form = CreateBlogPostForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                obj = form.save(commit=False)
                author = Account.objects.filter(email=user.email).first()
                obj.author = author
                obj.save()
                messages.success(request, f"Your Blog has been posted successfully!")
                return redirect("home")
            else:
                print(form)
                print("Invalid Form")
                print(form.errors)
                return render(request, "blog/create_blog.html", {"form": form})

        else:
            form = CreateBlogPostForm()
            context["form"] = form
        return render(request, "blog/create_blog.html", context)
    else:
        raise Http404("Page Not Found")


def detail_blog_view(request, slug):
    context = {}

    blog_post = get_object_or_404(BlogPost, slug=slug)
    context["blog_post"] = blog_post

    return render(request, "blog/detail_blog.html", context)


@login_required
def edit_blog_view(request, slug):

    context = {}
    user = request.user

    if not user.is_authenticated:
        return redirect("must_authenticate")

    blog_post = get_object_or_404(BlogPost, slug=slug)

    if blog_post.author != user:
        return HttpResponse("You are not the author of that post.")

    if request.POST:
        form = UpdateBlogPostForm(
            request.POST or None, request.FILES or None, instance=blog_post
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, f"Your Post has been updated successfully!")
            blog_post = obj
            return redirect("home")

    form = UpdateBlogPostForm(
        initial={
            "title": blog_post.title,
            "category": blog_post.category,
            "body": blog_post.body,
            "related_event": blog_post.related_event,
            "image": blog_post.image,
        }
    )

    context["form"] = form
    categorys = Category.objects.all()
    context["categorys"] = categorys
    event_posts = EventPost.objects.filter(author=user)
    context["event_posts"] = event_posts
    return render(request, "blog/edit_blog.html", context)


@login_required
def delete_blog_view(request, id):

    context = {}
    blog_post = get_object_or_404(BlogPost, id=id)
    if request.method == "POST":
        blog_post.delete()
        messages.success(request, f"Your Post has been deleted successfully!")
        return redirect("home")

    context["blog_post"] = blog_post
    return render(request, "blog/delete_blog.html", context)


def get_blog_queryset(query=None):
    queryset = []

    queries = query.split(" ")
    for q in queries:
        posts = BlogPost.objects.filter(
            Q(title__contains=q)
            | Q(body__icontains=q)
            | Q(author__username__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)

    # create unique set and then convert to list
    return list(set(queryset))
