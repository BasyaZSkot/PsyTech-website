from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class CustomSignup(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    specialyty = models.CharField(max_length=12, choices=(('psihologyst', "PSIHOLOGYST"), ('regular user', "REGULAR USER")), default='regular user', error_messages=None)
    profile_picture = models.ImageField(upload_to="images", error_messages=None)
    date_of_birth = models.DateField()

class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

class UserInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialyty = models.CharField(max_length=12, choices=(('psihologyst', "PSIHOLOGYST"), ('regular user', "REGULAR USER")), default='regular user', error_messages=None)
    profile_picture = models.ImageField(upload_to="images", error_messages=None)
    date_of_birth = models.DateField()

