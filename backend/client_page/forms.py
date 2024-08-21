from django import forms
from .models import UserPsihHelpInfo

class UserPsihHelpInfoForm(forms.ModelForm):
    class Meta:
        model = UserPsihHelpInfo
        fields = ["problems", "psih_gender", "psih_years_old", "price", "time"]