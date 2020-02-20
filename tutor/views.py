from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

def home(request):
    #return HttpResponse("This is the tutor homepage.")
    return render(request, 'tutor/home.html', {})


def login(request):
    #return HttpResponse("This is the login page.")
    return render(request, 'tutor/login.html', {})

def profile(request):
    #return HttpResponse("This is a profile page (profile model to come).")
    return render(request, 'tutor/profile.html', {})
