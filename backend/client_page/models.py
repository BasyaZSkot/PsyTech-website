from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProblems_and_Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    problems = models.CharField(max_length=100, choices=((("problems in relationsheep", "Проблемы в отношениях"),
                                                                               ("work/study", "Проф деятельность - учеба/работа"), 
                                                                               ("emotionale condition", "Эмоциональное состояние"), 
                                                                               ("another", "Другое"), 
                                                                               ("do not want to say", "Не хочу говорить"))), 
                                                                    )
    comment_ab_problem = models.CharField(max_length=255) 
    prefer_psih_gender = models.CharField(max_length=15, choices=(("male", "Male"), 
                                                                  ("female", "Female"),
                                                                  ("doesn't metter", "Не важно")
                                                                     ))
    prefer_psih_years_old = models.CharField(max_length=20, choices=(("25", "25 лет"), 
                                                                    ("25-35", "25-35 лет"), 
                                                                    ("35-45", "35-45 лет"), 
                                                                    ("45-55", "45-55 лет"), 
                                                                    ("55", "от 55 лет"), 
                                                                    ("doesn't metter", "без разницы")
                                                            )
                                                            )
    prefer_price = models.CharField(max_length=100, choices=(("3000", "3-х лет - от 3.000 рублей"), 
                                                                                         ("4000", "middle - от 4.000 рублей"), 
                                                                                         ("5000", "ведущий психолог с опытом от 5 лет - от 5.000 рублей"), 
                                                                                         ("doesn't metter", "Не важно")
                                                                                        ),)
    prefer_time_slots = models.CharField(max_length=255)
    prefer_notif = models.CharField(max_length=255, choices=(("email", "Email"), ("SMS", "SMS"), ("website", "Web Site Notifications")))
    prefered_method_for_chating = models.CharField(max_length=511)
  
    def __str__(self):
        return self.user.username
  
