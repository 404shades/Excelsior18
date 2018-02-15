from django.shortcuts import render, redirect
from .models import Participate
from Events.models import Event
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/accounts/login/')
def participate_home(request):
    part_obj, new_obj = Participate.objects.new_or_get(request)
    context = {
        "participation": part_obj
    }
    return render(request, "Participation/index.html", context)


@login_required(login_url='/accounts/login/')
def participate_update(request):
    event_id = request.POST.get('event_id')
    if event_id is not None:
        try:
            obj = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return redirect("Participation:home")
        part_obj, new_obj = Participate.objects.new_or_get(request)
        if obj in part_obj.eventspart.all():
            part_obj.eventspart.remove(obj)
        else:
            part_obj.eventspart.add(obj)
    return redirect("Participation:home")


