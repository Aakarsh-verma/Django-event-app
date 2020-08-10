from django.urls import path
from premium_event.views import (
    create_premium_event_view,
    detail_premium_event_view,
    edit_premium_event_view,
    delete_premium_event_view,
)


app_name = "premium_event"

urlpatterns = [
    path("create/", create_premium_event_view, name="create"),
    path("<slug>/", detail_premium_event_view, name="detail"),
    path("<slug>/edit", edit_premium_event_view, name="edit"),
    path("<int:id>/delete", delete_premium_event_view, name="delete"),
]
