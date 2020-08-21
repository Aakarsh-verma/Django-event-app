from django.urls import path
from event.views import (
    create_event_view,
    detail_event_view,
    edit_event_view,
    delete_event_view,
    apply_premium_view,
    confirm_apply_view,
    approve_premium_view,
    confirm_premium_view,
    create_profile_view,
    author_view,
)


app_name = "event"

urlpatterns = [
    path("create/", create_event_view, name="create"),
    # path("author/<int:id>/profile_pic", profile_update_view, name="update_pic"),
    path("profile/<int:id>/", create_profile_view, name="create-profile"),
    path("author/<int:id>/", author_view, name="author-view"),
    path("apply_premium/", apply_premium_view, name="apply_premium"),
    path("<slug>/confirm_apply/", confirm_apply_view, name="confirm_apply"),
    path("approve_premium/", approve_premium_view, name="approve_premium"),
    path("<slug>/confirm_premium/", confirm_premium_view, name="confirm_premium"),
    path("<slug>/", detail_event_view, name="detail"),
    path("<slug>/edit", edit_event_view, name="edit"),
    path("<int:id>/delete", delete_event_view, name="delete"),
]
