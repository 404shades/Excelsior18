from django.db import models
from django.conf import settings
from Events.models import Event
User = settings.AUTH_USER_MODEL
# Create your models here.


class Participate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Events = models.ManyToManyField(Event, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id