from django.shortcuts import render


# Create your views here.
def participate_home(request):
    return render(request, "Participation/index.html", {})
