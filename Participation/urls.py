from django.urls import path
from .views import participate_home

urlpatterns =[
    path('home/', participate_home, name='home'),
]