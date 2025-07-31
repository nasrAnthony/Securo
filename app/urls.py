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
    path('quote-form/', accounts_views.quote_request_view, name='quote'),
    path('login/', accounts_views.login, name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('register/', accounts_views.register, name='register'),
    path('my-profile/', accounts_views.profile_view, name='profile'), 
    path("quotes/<int:pk>/cancel/", accounts_views.cancel_quote, name="quote_cancel"),
    path('my-profile/edit', accounts_views.profile_edit, name='profile_edit'),
    path('my-profile/delete', accounts_views.delete_account, name='account_delete')
]
