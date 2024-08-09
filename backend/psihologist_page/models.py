from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Summary(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    degree = models.CharField(max_length=50, choices=(("Бакалавр", "bachelor"), ("Специалист", "specialist"), ("Магистр", "master")))

    universyty = models.CharField(max_length=100)
    diploma = models.FileField(upload_to="files")
    training = models.CharField(max_length=100)
    advanced_curses = models.CharField(max_length=200)

    description = models.TextField()

    science_interestings = models.CharField(max_length=500)

    achievements = models.CharField(max_length=200)

    work_area = models.CharField(max_length=100)

    often_questions = models.CharField(max_length=200)

    experience = models.CharField(max_length=2, choices=(("1", "1"), ("2","2"), ("3", "3"), ("4", "4"), ("5+","5+")))

    something_to_add = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.user.username
    
class SummaryDescription(models.Model):
    inspector = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE)

    def __str__(self):
        return self.inspector.username

class SubscribesPrice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    per_session = models.IntegerField()

    def __str__(self) -> str:
        return self.user.username

class FreePlaces(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    free_places = models.CharField(max_length=4700)

    def __str__(self):
        return self.user.username
    
class SessionsDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dates = models.CharField(max_length=4700)

    def __str__(self):
        return self.user.username