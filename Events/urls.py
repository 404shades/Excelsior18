from django.urls import path
from .views import EventsView, EventListView, EventContactTeam, TechnicalEventList, TechnicalContactTeam, allrules, technicalRules
app_name = "Events"
urlpatterns = [
    path('allevents/', EventsView.as_view(), name='events'),
    path('allevents/<slug:slug>/', EventListView.as_view()),
    path('allevents/<slug:slug>/contact', EventContactTeam.as_view(), name='contact-team'),
    path('allevents/<slug:slug>/<slug:slug2>', TechnicalEventList.as_view()),
    path('allevents/<slug:slug>/<slug:slug2>/excelsior/rules', technicalRules),
    path('allevents/<slug:slug>/<slug:slug2>/contact', TechnicalContactTeam.as_view()),
    path('allevents/<slug:slug>/excelsior/rules', allrules),
]
