from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import *
from django.shortcuts import get_object_or_404
from .models import Event
import re
from Participation.models import Participate

# Create your views here.


class EventsView(TemplateView):
    template_name = 'Events/AllEvents.html'
    # queryset = Event.objects.all()
    #
    # def get_context_data(self, **kwargs):
    #     context = super(EventsView,self).get_context_data(**kwargs)
    #     request = self.request
    #     if request.user.is_authenticated:
    #         parting, newing = Participate.objects.new_or_get(request)
    #         context['participate'] = parting
    #         return context
    #     return context


class EventListView(ListView):
    template_name = 'Single Event/index.html'

    def get_queryset(self):
        categ = get_object_or_404(Category,slug=self.kwargs['slug'])
        sub_categ = categ.subcategory_set.all()
        if sub_categ.exists():
            if sub_categ.count()==1:
                elem = sub_categ.first()
                qs = elem.event_set.all()
                return qs
            else:
                qs = sub_categ
                return qs
        else:
            return None

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(EventListView,self).get_context_data(**kwargs)
        categ = get_object_or_404(Category, slug=self.kwargs['slug'])
        heading = categ.title.split(' ', 1)[0].capitalize()
        request = self.request
        if request.user.is_authenticated:
            parting, newing = Participate.objects.new_or_get(request)
            data['participate'] = parting
        data['heading'] = heading
        data['urling'] = categ.slug
        return data


class EventContactTeam(ListView):
    queryset = Category.objects.all()
    template_name = 'Single Event/generic.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(EventContactTeam,self).get_context_data(**kwargs)
        categ = get_object_or_404(Category, slug=self.kwargs['slug'])
        data['head'] = categ.title.split(' ', 1)[0].capitalize()
        data['contact_team_name'] = categ.team_head_name.split(",")
        data['contact_team_mobile'] = categ.team_head_mobile.split(",")
        data['urlfu'] = categ.slug
        return data


