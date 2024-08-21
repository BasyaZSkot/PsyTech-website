from django.urls import path
from . import views

urlpatterns = [
    path("additionaly/", views.additionaly_regular_user, name="regular_user_additonaly")
]
