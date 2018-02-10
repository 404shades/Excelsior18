from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import FormView

from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model
# Create your views here.
User = get_user_model()


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('UserName')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        else:
            print('Error')
    return render(request, 'Authentication/login.html', context)


class RegisterView(FormView):
    form_class = RegisterForm
    success_url = '/accounts/login'
    template_name = 'Authentication/register.html'

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        email = self.request.POST['email']
        User.objects.create_user(username=username, email=email, password=password)
        return super(RegisterView, self).form_valid(form)