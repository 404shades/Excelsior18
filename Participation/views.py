from django.shortcuts import render, redirect
from .models import Participate
from Events.models import Event
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/accounts/login/')
def participate_home(request):
    part_obj, new_obj = Participate.objects.new_or_get(request)
    return render(request, "Participation/index.html", {})


@login_required(login_url='/accounts/login/')
def participate_update(request):
    obj = Event.objects.get(id=2)
    part_obj, new_obj = Participate.objects.new_or_get(request)
    if obj in part_obj.eventspart.all():
        part_obj.eventspart.remove(obj)
    else:
        part_obj.eventspart.add(obj)
    return redirect("Participation:home")


