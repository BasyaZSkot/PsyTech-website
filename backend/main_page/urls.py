from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('psihologysts/<int:pk>', views.psihologyst_detail_view, name="psihologyst_detail_view"),
    path('settings/', views.settings, name="settings"),
    path('settings/user_information', views.user_information, name="user_information"),
    path('settings/summary', views.summary_settings, name="summary_settings"),
    path('settings/change_password/', views.change_password, name="change_password"),
    path('additionaly-info/', views.additionaly, name='additionaly')
    ]


