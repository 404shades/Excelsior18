from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginForm(forms.Form):
    UserName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        password_confirm = data.get('password2')
        if password != password_confirm:
            raise ValidationError('Passwords do not match')
        return data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise ValidationError('Username Already Used')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise ValidationError('Email Already In Use')
        return email

