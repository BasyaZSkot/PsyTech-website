from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>', views.chat, name="chat"),
    path('mark_as_read/<int:pk>', views.mark_as_read, name="mark_as_read"),
    path('save/', views.save, name="save")
]