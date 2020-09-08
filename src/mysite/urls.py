from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from personal.views import (
    home_screen_view,
    event_home_screen_view,
    premium_event_screen_view,
    committee_home_screen_view,
)

from account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    must_authenticate_view,
    limit_reached_view,
)

urlpatterns = [
    path("", event_home_screen_view, name="event-home"),
    path("blog_home/", home_screen_view, name="home"),
    path("admin/", admin.site.urls),
    path("account/", account_view, name="account"),
    path("blog/", include("blog.urls", "blog")),
    path("premium_events/", premium_event_screen_view, name="premium-events"),
    path("event/", include("event.urls", "event")),
    path("committee_home/", committee_home_screen_view, name="committee-home"),
    path("committee/", include("committee.urls", "committee")),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("must_authenticate/", must_authenticate_view, name="must_authenticate"),
    path("limit_reached/", limit_reached_view, name="limit_reached"),
    path("register/", registration_view, name="register"),
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change.html"
        ),
        name="password_change",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
