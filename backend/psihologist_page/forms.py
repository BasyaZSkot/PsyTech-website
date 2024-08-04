from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Summary, SummaryDescription, SubscribesPrice
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

class SubscribesForm(forms.ModelForm):
    class Meta:
        model = SubscribesPrice
        fields = ["per_session"]

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].help_text = None
