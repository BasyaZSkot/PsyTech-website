from django import forms
from .models import UserInformation
from allauth.account.forms import SignupForm

class DateInput(forms.DateInput):
    input_type = 'date'

class UserInformationForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = ["gender", "specialyty", "date_of_birth", "profile_picture", "expirience", "about"]
        widget = {
            "date_of_birth": DateInput()
        }
