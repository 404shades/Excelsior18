from django.urls import path
from .views import participate_update, Profile


app_name = 'Participation'


urlpatterns =[
    path('update/', participate_update, name='update'),
    path('profile', Profile.as_view(), name='profile'),
]