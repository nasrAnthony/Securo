# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'), 
    path('camera-systems/', views.camera_systems, name='systemcamera'),
    path('alarm-systems/', views.alarm_systems, name='systemalarm'),
    path('login/', views.login, name='login'),
    path('quote-form/', views.quote, name='quote')
]
