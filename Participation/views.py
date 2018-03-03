from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Participate
from Events.models import Event
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


def participate_detail_api_view(request):
    part_obj, new_obj = Participate.objects.new_or_get(request)
    eventsmate = [{"title": x.title,"ide": x.id} for x in part_obj.eventspart.all()]
    jsondata = {
        'eventsring':eventsmate
    }
    print(jsondata)
    return JsonResponse(jsondata)


# @login_required(login_url='/accounts/login/')
# def participate_home(request):
#     part_obj, new_obj = Participate.objects.new_or_get(request)
#     context = {
#         "participation": part_obj
#     }
#     return render(request, "Participation/index.html", context)


@login_required(login_url='/accounts/login/')
def participate_update(request):
    event_id = request.POST.get('event_id')
    if event_id is not None:
        try:
            obj = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return redirect("Participation:profile")
        part_obj, new_obj = Participate.objects.new_or_get(request)
        if obj in part_obj.eventspart.all():
            part_obj.eventspart.remove(obj)
            part_added = False
        else:
            part_obj.eventspart.add(obj)
            part_added = True
        if request.is_ajax():
            print("Ajax Request")
            jsonData ={
                "added": part_added,
                "removed": not part_added,
            }
            return JsonResponse(jsonData)
    return redirect("Participation:profile")


class Profile(LoginRequiredMixin,ListView):
    template_name = 'Profile/index.html'

    def get_queryset(self):
        qs = Participate.objects.new_or_get(self.request)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(Profile, self).get_context_data(**kwargs)
        data['profil']  = self.request.user
        part_obj, newing = Participate.objects.new_or_get(self.request)
        data['participation'] =  part_obj
        return data

