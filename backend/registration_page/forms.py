from django import forms
from .models import UserRegistration, UserInformation

class DateInput(forms.DateInput):
    input_type = 'date'

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserRegistration
        fields = ("username", "first_name", "last_name", "email", "password")

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserRegistration
        fields = ("username", "password")

class UserInformationForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = UserInformation
        fields = ['specialyty', 'profile_picture', 'date_of_birth']
        widgets = {
            'date_of_birth': DateInput(),
        }

class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = ["password"]