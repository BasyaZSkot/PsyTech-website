from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserPsihHelpInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problems = models.CharField(max_length=100, choices=((("problems in relationsheep", "проблемы в отношениях"), ("work/study", "проф деятельность - учеба/работа"), ("emotionale condition", "эмоциональное состояние"), ("another", "другое"), ("do not want to say", "не хочу говорить"))))
    psih_gender = models.CharField(max_length=15, choices=(("men", "MEN"), ("women", "WOMEN"), ("does not metter", "без разницы")))
    psih_years_old = models.CharField(max_length=20, choices=(("25", "25 лет"), ("25-35", "25-35 лет"), ("35-45", "35-45 лет"), ("45-55", "45-55 лет"), ("55", "от 55 лет"), ("does not metter", "без разницы")))
    price = models.CharField(max_length=100, choices=((3000, "3-х лет - от 3.000 рублей"), (4000, "middle - от 4.000 рублей"), (5000, "ведущий психолог с опытом от 5 лет - от 5.000 рублей")))
    time = models.TimeField()