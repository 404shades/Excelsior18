from django.db import models
from django.conf import settings
from Events.models import Event
User = settings.AUTH_USER_MODEL
# Create your models here.


class ParticipateManager(models.Manager):
    def new_or_get(self, request):
        if request.user.is_authenticated:
            userhead = request.user
            part = self.get_queryset().filter(user=userhead)
            if part.count() == 1:
                new_obj = False
                print("Already Exists")
                part_obj = part.first()
            else:
                print(part.count())
                part_obj = Participate.objects.new_participate(user=userhead)
                new_obj = True
                print("New Creation")
            return part_obj, new_obj

    def new_participate(self, user):
        return self.model.objects.create(user=user)


class Participate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    eventspart = models.ManyToManyField(Event, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name
    objects = ParticipateManager()
