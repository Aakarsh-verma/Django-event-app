from django.urls import path
from event.views import (
    create_event_view,
    detail_event_view,
    edit_event_view,
)


app_name = "event"

urlpatterns = [
    path("create/", create_event_view, name="create"),
    path("<slug>/", detail_event_view, name="detail"),
    path("<slug>/edit", edit_event_view, name="edit"),
]
