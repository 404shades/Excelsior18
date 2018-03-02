from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import FormView, CreateView
import sendotp
from .forms import LoginForm, RegisterForm, VerificationForm
from django.contrib.auth import authenticate, login, get_user_model, logout
# Create your views here.
import json
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
    success_url = '/accounts/verify/'
    template_name = 'Authentication/register.html'

    def form_valid(self, form):
        print(form.cleaned_data)
        request = self.request
        request.session['user_one'] = form.cleaned_data.get('email')
        form.save()
        return redirect('/accounts/verify/')
    # def post(self, request, *args, **kwargs):
    #     print("welcome Rohan Malik")
    #     user = self.request.POST['full_name']
    #     print(user)
    #     mob_no = self.request.POST['mobile_no'].strip("+")
    #     otp_obj = sendotp.sendotp.sendotp('197589AXDtCunMpPbM5a7eba71',
    #                                       'Hello ' + user + '\nThank You For Signing Up with Excelsior 2018, \n{{otp}} is the OTP for your Registration Process. This is usable once and valid for 5 minutes from the request. \nPlease donot share it with anyone...\n\nLike Our Facebook Page https://www.facebook.com/excelsior.uiet \nFollow us on Instagram https://www.instagram.com/excelsioruiet')
    #     otp = otp_obj.generateOtp()
    #     otp_obj.send(mob_no, 'EXCLSR', otp)
    #     return redirect('/accounts/login')


def logout_view(request):
    logout(request)
    return redirect('/')


class VerificationOTP(FormView):
    form_class = VerificationForm
    template_name = 'Authentication/verify.html'

    def form_valid(self, form):
        request = self.request
        user = User.objects.get(email=request.session.get('user_one'))
        otpobj = sendotp.sendotp.sendotp('197589AXDtCunMpPbM5a7eba71','')
        mobile_no = user.get_mobile().strip("+")
        otp = form.cleaned_data.get("otpinput")
        js = otpobj.verify(mobile_no, otp)
        print(type(js))
        if js==200:
            user.active = True
            print(user)
            del request.session['user_one']
            return redirect('/accounts/login/')
        else:
            print('CHLL Be Chutie')
            super(VerificationOTP,self).form_invalid(form)
