from django.urls import path
from committee.views import (
    detail_committee_view,
    edit_committee_view,
)


app_name = "committee"

urlpatterns = [
    path("<slug>/", detail_committee_view, name="detail"),
    path("<slug>/edit", edit_committee_view, name="edit"),
]
