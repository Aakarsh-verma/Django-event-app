from django.urls import path
from committee.views import (
    detail_committee_view,
    edit_committee_view,
    )
from personal.views import committee_home_screen_view


app_name = 'committee'

urlpatterns =[
    path('committee_home/', committee_home_screen_view, name='committee-home'),
    path('<slug>/', detail_committee_view, name='detail'),
    path('<slug>/edit', edit_committee_view, name='edit'),
]
