from django.contrib import admin
from .models import Summary, SummaryDescription, SubscribesPrice, FreePlaces, SessionsDate, Universyty, Practise

# Register your models here.
admin.site.register(Summary)
admin.site.register(SummaryDescription)
admin.site.register(SubscribesPrice)
admin.site.register(FreePlaces)
admin.site.register(SessionsDate)
admin.site.register(Universyty)
admin.site.register(Practise)