from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Profile

def home(request):
	tutors = Profile.objects.all()
	context = {'tutors': tutors}
	return render(request, 'tutor/home.html', context)

def login(request):
    return render(request, 'tutor/login.html', {})

def profile(request):
    return render(request, 'tutor/profile.html', {})
