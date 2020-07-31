from django.urls import path
from event.views import (
    detail_event_view,
    edit_event_view,
    )
from personal.views import event_home_screen_view

app_name = 'event'

urlpatterns =[
    path('event_home/', event_home_screen_view, name='event-home'),
    path('<slug>/', detail_event_view, name='detail'),
    path('<slug>/edit', edit_event_view, name='edit'),
]
