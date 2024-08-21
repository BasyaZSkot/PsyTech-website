from django.db import models
from django.contrib.auth.models import User    

class Universyty(models.Model):
    # user = models.ForeignKey(User, related_name='user_a', on_delete=models.CASCADE)
    end_year = models.IntegerField()
    referal = models.CharField(max_length=100)
    degree = models.CharField(max_length=50, choices=(("Бакалавр", "bachelor"), ("Специалист", "specialist"), ("Магистр", "master")))
    facs = models.CharField(max_length=100)
    universyty = models.CharField(max_length=100)
    diploma = models.FileField(upload_to="files")
    
class Practise(models.Model):
    start_year = models.DateField()
    clients_count = models.CharField(max_length=100, help_text="You can write an intervele")
    online_expirience = models.BooleanField()
    self_terapy = models.BooleanField()
    supervisore_have = models.BooleanField()
    supervisore_recomindation = models.FileField()
    additional_work_studing = models.CharField(max_length=100)
    clients_count_on_platform = models.CharField(max_length=100, help_text="You can write an intervele")


class Summary(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    advanced_study = models.CharField(max_length=200)
    additional_studing = models.CharField(max_length=100)
    universyty = models.ManyToManyField(Universyty)
    practise = models.ForeignKey(Practise, on_delete=models.CASCADE)
    expirience = models.IntegerField()
    
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_dates")
    psih = models.ForeignKey(User, on_delete=models.CASCADE, related_name="psih")
    dates = models.CharField(max_length=4700)

    def __str__(self):
        return self.user.username+"<-"+self.psih.username