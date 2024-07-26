from django import forms
from .models import UserInformation, CustomSignup

class DateInput(forms.DateInput):
    input_type = 'date'

class EmailConfirmationForm(forms.Form):
    token = forms.CharField(max_length=8)

class UserInformationForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = ['specialyty', 'profile_picture', 'date_of_birth']
        widgets = {
            'date_of_birth': DateInput(),
        }

class CustomSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=50, widget=forms. TextInput({ "placeholder": "Username"}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput({ "placeholder": "Password"}))
    specialyty = forms.CharField(widget=forms.Select({'class': 'custom-dropdown'}, choices=(('regular user', "REGULAR USER"), ('psihologyst', "PSIHOLOGYST"))))
    class Meta:
        model = CustomSignup
        fields = ['username', 'password', 'specialyty', 'profile_picture', 'date_of_birth']
        widgets = {
            'date_of_birth': DateInput(), 
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
    def save(self, request):
        user = super(CustomSignupForm, self).save()
        user_info = UserInformation(user=user, specialty=self.cleaned_data['specialty'], profile_picture=self.cleaned_data['profile_picture'], date_of_birth=self.cleaned_data['date_of_birth'])
        user_info.save()
        return user

class ChangePasswordForm(forms.ModelForm):
    password = forms.PasswordInput()