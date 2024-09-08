from django.urls import path
from . import views

urlpatterns = [
    path("additionaly/", views.additionaly_regular_user, name="regular_user_additonaly"),
    path("client-info/<int:cl_id>", views.client_info_page, name="client_info")
]
