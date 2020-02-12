from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("This is the tutor homepage.")

def login(request):
    return HttpResponse("This is the login page.")

def profile(request):
    return HttpResponse("This is a profile page (profile model to come).")