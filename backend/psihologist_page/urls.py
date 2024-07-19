from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('<int:pk>/', views.SummaryDetailView.as_view(), name="summaries_view"),
    path('filling/', views.getting_summary, name="filling_summary"),
    path('<int:pk>/reject-summary/', views.reject_summary, name="reject_summary"),
    path('<int:pk>/confirm/', views.confirm_summary, name="confirm_summary"),
    path('summary_mistakes/<int:pk>', views.summary_mistakes, name='summary_mistakes'),
    path('summary_mistakes_view/<int:pk>', views.summary_description_detail_view, name="summary_mistakes_view"),
]