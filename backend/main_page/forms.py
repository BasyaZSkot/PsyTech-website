from django import forms
from .models import UserInformation

class DateInput(forms.DateInput):
    input_type = 'date'

class UserInformationForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = ["gender", "specialyty", "date_of_birth", "profile_picture",]
        widget = {
            "date_of_birth": DateInput()
        }