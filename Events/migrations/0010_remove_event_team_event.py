# Generated by Django 2.0.2 on 2018-03-05 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0009_event_team_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='team_event',
        ),
    ]
