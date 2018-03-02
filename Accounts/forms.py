from django import forms
from django.core.exceptions import ValidationError
import sendotp
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'mobile_no', 'roll_no')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin', 'full_name', 'mobile_no', 'roll_no')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'mobile_no', 'roll_no')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.active = False
        if commit:
            print("welcome Rohan Malik")
            username = user.get_full_name()
            print(user)
            mob_no = user.get_mobile().strip("+")
            otp_obj = sendotp.sendotp.sendotp('197589AXDtCunMpPbM5a7eba71',
                                              'Hello ' + username + '\nThank You For Signing Up with Excelsior 2018, \n{{otp}} is the OTP for your Registration Process.')
            otp = otp_obj.generateOtp()
            otp_obj.send(mob_no, 'EXCLSR', otp)
            user.save()
        return user


class VerificationForm(forms.Form):
    otpinput = forms.CharField(label='Enter OTP RECEIVED', widget=forms.PasswordInput)

    def clean_otpinput(self):
        otp = self.cleaned_data.get('otpinput')
        if len(otp)>4:
            raise forms.ValidationError("Abe bewade pee rakhi h kya bc 4 akshar se bda dalega")
        return otp
