from django import forms
from .models import UserInformation

class DateInput(forms.DateInput):
    input_type = 'date'

class EmailConfirmationForm(forms.Form):
    token = forms.CharField(max_length=8)

class UserInformationForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = UserInformation
        fields = ['specialyty', 'profile_picture', 'date_of_birth']
        widgets = {
            'date_of_birth': DateInput(),
        }

class ChangePasswordForm(forms.ModelForm):
    password = forms.PasswordInput()