from django.contrib import admin
from .models import UserInformation, EmailConfirmation

admin.site.register(UserInformation)
admin.site.register(EmailConfirmation)