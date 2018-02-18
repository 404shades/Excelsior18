from django.shortcuts import render
from django.views.generic import ListView
from .models import Event
from Participation.models import Participate

# Create your views here.


class EventsView(ListView):
    template_name = 'Events/listshow.html'
    queryset = Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super(EventsView,self).get_context_data(**kwargs)
        request = self.request
        if request.user.is_authenticated:
            parting, newing = Participate.objects.new_or_get(request)
            context['participate'] = parting
            return context
        return context
