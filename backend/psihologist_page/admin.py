from django.contrib import admin
from .models import Summary, SummaryDescription, SubscribesPrice, FreePlaces

# Register your models here.
admin.site.register(Summary)
admin.site.register(SummaryDescription)
admin.site.register(SubscribesPrice)
admin.site.register(FreePlaces)
