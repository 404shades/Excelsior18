from django.urls import path
from .views import login_page, RegisterView

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', RegisterView.as_view(), name='register')
]
