from django.urls import path
from .views import LoginView, RegisterView, logout_view, VerificationOTP
app_name = 'Accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('verify/', VerificationOTP.as_view(), name='verify'),
]
