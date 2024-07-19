from django import forms
from .models import Summary, SummaryDescription

class SummaryForm(forms.ModelForm):
    username = forms.CharField(required=False)
    something_to_add = forms.CharField(required=False)
    class Meta:
        model = Summary
        fields = ("degree",
                  "universyty",
                  "diploma",
                  "training",
                  "advanced_curses",
                  "description",
                  "science_interestings",
                  "achievements",
                  "work_area",
                  "often_questions",
                  "experience",
                  "something_to_add",
                )


class SummaryDescriptionForm(forms.ModelForm):
    class Meta:
        model = SummaryDescription
        fields = ("description",)