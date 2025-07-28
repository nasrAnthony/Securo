# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'), 
    path('installation/', views.installation_service, name='systemcamera'),
    path('login/', views.login, name='login'),
    path('quote-form/', views.quote, name='quote')
]
