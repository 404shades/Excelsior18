from django.urls import path
from .views import EventsView, EventListView, EventContactTeam
app_name = "Events"
urlpatterns = [
    path('allevents/', EventsView.as_view(), name='events'),
    path('allevents/<slug:slug>/', EventListView.as_view()),
    path('allevents/<slug:slug>/contact', EventContactTeam.as_view(), name='contact-team'),
]
