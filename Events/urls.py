from django.urls import path
from .views import EventsView

urlpatterns = [
    path('general/', EventsView.as_view(), name='general'),
]
