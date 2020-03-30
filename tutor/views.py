from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Profile

@login_required
def home(request):
	tutors = Profile.objects.filter(active=True)
	context = {'tutors': tutors}
	return render(request, 'tutor/home.html', context)

def login(request):
    return render(request, 'tutor/login.html', {})
