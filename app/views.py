from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# app/views.py

def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def camera_systems(request):
    return render(request, 'camsystems.html')

def alarm_systems(request):
    return render(request, 'alarmsystems.html')

