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
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', accounts_views.register, name='register'),
]
