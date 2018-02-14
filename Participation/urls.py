from django.urls import path
from .views import participate_home, participate_update


app_name = 'Participation'


urlpatterns =[
    path('home/', participate_home, name='home'),
    path('update/', participate_update, name='update'),
]