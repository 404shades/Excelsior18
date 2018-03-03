from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import *
from django.shortcuts import get_object_or_404
from django.http import Http404
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
        technical = False
        categ = get_object_or_404(Category, slug=self.kwargs['slug'])
        sub_categ = categ.subcategory_set.all()
        if sub_categ.exists():
            if sub_categ.count() > 1:
                technical = True
        heading = categ.title.split(' ', 1)[0].capitalize()
        request = self.request
        if request.user.is_authenticated:
            parting, newing = Participate.objects.new_or_get(request)
            data['participate'] = parting
        data['heading'] = heading
        data['urling'] = categ.slug
        data['technical'] = technical
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


class TechnicalEventList(ListView):
    template_name = 'Single Event/index.html'

    def get_queryset(self):
        categ = get_object_or_404(Category, slug = self.kwargs['slug'])
        sub_categ = categ.subcategory_set.all()
        events = None
        print(sub_categ.count())
        if sub_categ.exists():
            if sub_categ.count() != 1:
                print(self.kwargs['slug2'])
                accli = get_object_or_404(SubCategory, slug=self.kwargs['slug2'])
                events = accli.event_set.all()
                return events
        return events

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(TechnicalEventList, self).get_context_data(**kwargs)
        technical = False
        categ = get_object_or_404(Category, slug=self.kwargs['slug'])
        sub_categ = get_object_or_404(SubCategory, slug=self.kwargs['slug2'])
        heading = sub_categ.title.split(' ', 1)[0].capitalize()
        request = self.request
        if request.user.is_authenticated:
            parting, newing = Participate.objects.new_or_get(request)
            data['participate'] = parting
        data['sub_event'] = True
        data['heading'] = heading
        data['categ_slug'] = categ.slug
        data['urling'] = sub_categ.slug
        data['technical'] = technical
        return data


class TechnicalContactTeam(ListView):
    queryset = Category.objects.all()
    template_name = 'Single Event/generic.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(TechnicalContactTeam,self).get_context_data(**kwargs)
        categ = get_object_or_404(Category, slug=self.kwargs['slug'])
        sub = get_object_or_404(SubCategory, slug=self.kwargs['slug2'])
        data['head'] = sub.title.split(' ', 1)[0].capitalize()
        data['contact_team_name'] = categ.team_head_name.split(",")
        data['contact_team_mobile'] = categ.team_head_mobile.split(",")
        data['urlfu'] = categ.slug
        data['urlsub'] = sub.slug
        data['subcat'] = True
        return data


def allrules(request, **kwargs):
    slug = kwargs['slug']
    categ = get_object_or_404(Category, slug=slug)
    print(slug)
    context = {
        "heading": categ.title.split(' ', 1)[0].capitalize(),
        "urlcateg":categ.slug,

    }
    if categ.title.lower() == 'general events':
        return render(request,'Single Event/general.html',context)
    elif categ.title.lower() == 'cultural events':
        return render(request, 'Single Event/cultural.html', context)
    elif categ.title.lower() == 'technical events':
        return render(request, 'Single Event/cultural.html', context)
    else:
        raise Http404


def technicalRules(request, **kwargs):
    slug = kwargs['slug']
    slug2 = kwargs['slug2']
    categ = get_object_or_404(Category, slug=slug)
    sub_categ = get_object_or_404(SubCategory, slug=slug2)
    context = {
        "heading": categ.title.split(' ',1)[0].capitalize(),
        "urlcateg": categ.slug,
        "urlsub": sub_categ.slug,
        "subevent": True
    }
    print(sub_categ.title)
    if sub_categ.title.lower() == 'takneek':
        return render(request, 'Single Event/takneek.html', context)
    elif sub_categ.title.lower() == 'throttle':
        return render(request, 'Single Event/throttl.html', context)
    elif sub_categ.title.lower() == 'bioles':
        return render(request, 'Single Event/bioles.html', context)
    elif sub_categ.title.lower() == 'acclivity':
        return render(request, 'Single Event/acclivity.html', context)
    else:
        raise Http404
