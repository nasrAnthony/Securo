# app/urls.py
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'), 
    path('installation/', views.installation_service, name='systemcamera'),
    path('quote-form/', views.quote, name='quote'),
    path('login/', accounts_views.login, name='login'),
    path('logout/', accounts_views.logout, name='logout'),
    path('register/', accounts_views.register, name='register'),
]
