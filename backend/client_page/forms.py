from django import forms
from .models import UserProblems_and_Preferences

class UserPsihHelpInfoForm(forms.ModelForm):
    problems = forms.CharField(label="Problem:", widget=forms.Select(choices=((("problems in relationsheep", "Проблемы в отношениях"),
                                                                               ("work/study", "Проф деятельность - учеба/работа"), 
                                                                               ("emotionale condition", "Эмоциональное состояние"), 
                                                                               ("another", "Другое"), 
                                                                               ("do not want to say", "Не хочу говорить"))), 
                                                                    attrs={
                                                                        "class": "block w-full px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm", 
                                                                        "id": "problems",
                                                                        "rows": "3",
                                                                    }
                                                                )
                                                            )
    comment_ab_problem = forms.CharField(label="Comment about problem:", widget=forms.Textarea(attrs={
                                                                            "class": "block w-full px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm", 
                                                                            "id": "comment_ab_problem", 
                                                                            "rows": "3", 
                                                                            "placeholder": "Additional comments"
                                                                    }
                                                                )
                                                            )
    prefer_psih_gender = forms.CharField(label="Preferred Psychologist Gender", 
                                         widget=forms.Select(choices=(("male", "Male"), 
                                                                      ("female", "Female"),
                                                                      ("doesn't metter", "Не важно")
                                                                     ),
                                                             attrs={
                                                                    "class": "block w-full px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                                                                    "id": "prefer_psih_gender",
                                                                    "rows": "3",
                                                                   }
                                                                )
                                                            )
    prefer_psih_years_old = forms.CharField(label="Preferred Psychologist Age", widget=forms.Select(choices=(("25", "25 лет"), 
                                                                                                             ("25-35", "25-35 лет"), 
                                                                                                             ("35-45", "35-45 лет"), 
                                                                                                             ("45-55", "45-55 лет"), 
                                                                                                             ("55", "от 55 лет"), 
                                                                                                             ("doesn't metter", "без разницы")
                                                                                                            ),
                                                                                                    attrs={
                                                                                                        "class": "block w-full px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm", 
                                                                                                        "id": "prefer_psih_years_old",
                                                                                                        "rows": "3", 
                                                                                                    }
                                                                                                        )
                                                                                                    )
    prefer_price = forms.CharField(label="Preferred Price", widget=forms.Select(choices=(("3000", "3-х лет - от 3.000 рублей"), 
                                                                                         ("4000", "middle - от 4.000 рублей"), 
                                                                                         ("5000", "ведущий психолог с опытом от 5 лет - от 5.000 рублей"), 
                                                                                         ("doesn't metter", "Не важно")
                                                                                        ),
                                                                                attrs={
                                                                                    "class": "block w-full px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm", 
                                                                                    "id": "prefer_price", 
                                                                                    "rows": "3",
                                                                                }
                                                                            )
                                                                        )
    prefer_notif = forms.CharField(label="Preferred Notifycations Type", widget=forms.Select(choices=(("Email", "Email"), ("SMS", "SMS"), ("website", "Web Site Notifications")),
                                                                                attrs={
                                                                                    "class": "block w-full px-3 py-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm", 
                                                                                    "id": "prefer_notif", 
                                                                                    "rows": "3",
                                                                                }
                                                                            )
                                                                        )


    class Meta:
        model = UserProblems_and_Preferences
        fields = ["problems", "comment_ab_problem", "prefer_psih_gender", "prefer_psih_years_old", "prefer_price", "prefer_notif"]