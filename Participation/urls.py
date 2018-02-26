from django.urls import path
from .views import participate_home, participate_update, Profile


app_name = 'Participation'


urlpatterns =[
    path('home/', participate_home, name='home'),
    path('update/', participate_update, name='update'),
    path('profile', Profile.as_view(), name='profile'),
]