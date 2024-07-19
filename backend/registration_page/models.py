from django.db import models
from django.contrib.auth.models import User

class UserRegistration(models.Model):
    username = models.CharField(max_length=20, blank=True, error_messages=None)
    first_name =  models.CharField(max_length=20, blank=True, error_messages=None) 
    last_name = models.CharField(max_length=20, blank=True, error_messages=None)
    email = models.EmailField(max_length=100, blank=True, error_messages=None)
    password = models.CharField(max_length=50, error_messages=None)

    def __str__(self) -> str:
        return self.username

class UserInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialyty = models.CharField(max_length=12, choices=(('psihologyst', "PSIHOLOGYST"), ('regular user', "REGULAR USER")), default='regular user', error_messages=None)
    profile_picture = models.ImageField(upload_to="images", error_messages=None)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username
