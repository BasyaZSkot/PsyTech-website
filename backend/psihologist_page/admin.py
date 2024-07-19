from django.contrib import admin
from .models import Summary, SummaryDescription

# Register your models here.
admin.site.register(Summary)
admin.site.register(SummaryDescription)