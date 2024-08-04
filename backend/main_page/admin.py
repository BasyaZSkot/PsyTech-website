from django.contrib import admin
from .models import SystemMessages, UserInformation, Subscribe

admin.site.register(SystemMessages)
admin.site.register(UserInformation)
admin.site.register(Subscribe)