from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import FormView, CreateView
import sendotp
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model
# Create your views here.
User = get_user_model()


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'Authentication/index.html'

    def form_valid(self, form):
        next_ = self.request.GET.get('next')
        next_post = self.request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            if is_safe_url(redirect_path, self.request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = '/accounts/login'
    template_name = 'Authentication/register.html'


