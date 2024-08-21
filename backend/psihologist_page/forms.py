from typing import Any, Sequence
from django import forms
from .models import Summary, SummaryDescription, SubscribesPrice, Universyty, Practise

class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ("advanced_study",
                  "additional_studing",
                  "expirience"
        )

class UniversytyForm(forms.ModelForm):
    class Meta:
        model = Universyty
        fields = ("end_year", "referal", "degree", "facs", "universyty", "diploma")

class PractiseForm(forms.ModelForm):
    class Meta:
        model = Practise
        fields = ("start_year", 
                  "clients_count", 
                  "online_expirience", 
                  "self_terapy", 
                  "supervisore_have", 
                  "supervisore_recomindation", 
                  "additional_work_studing", 
                  "clients_count_on_platform")

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

UniversytyFormSet = forms.modelformset_factory(Universyty, fields=("end_year", "referal", "degree", "facs", "universyty", "diploma"), form=UniversytyForm, extra=1)