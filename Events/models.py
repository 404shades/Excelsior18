from django.db import models
import random
import os
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


def get_file_extension(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1, 3939292911)
    name, ext = get_file_extension(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class Category(models.Model):
    title = models.CharField(max_length=100)
    team_head_name = models.CharField(max_length=100)
    team_head_mobile = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100, default='Computer Science and Engineering')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class EventsManager(models.Manager):
    def get_by_id(self, ide):
        qs = self.get_queryset().filter(id=ide)
        if qs.count()==1:
            return qs.first()
        return None


class Event(models.Model):
    title = models.CharField(max_length=100)
    area = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    summary = models.TextField(max_length=4000)
    rules = models.TextField(max_length=4000)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.title

    objects = EventsManager()


