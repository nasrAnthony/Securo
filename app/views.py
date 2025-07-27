from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# app/views.py

def home(request):
    return HttpResponse("Welcome to the Securo Home page!")

def contact(request):
    return HttpResponse("Welcome to the Securo Contact page!")

def about(request):
    return HttpResponse("Welcome to the Securo About page!")
