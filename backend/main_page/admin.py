from django.contrib import admin
from .models import SystemMessages, UserInformation

admin.site.register(SystemMessages)
admin.site.register(UserInformation)