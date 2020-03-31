from django.shortcuts import render, redirect

from users.models import Profile
from tutor.forms import RequestForm
from tutor.models import Ask

def home(request):
	tutors = Profile.objects.filter(active=True)
	context = {'tutors': tutors}
	return render(request, 'tutor/home.html', context)

def login(request):
    return render(request, 'tutor/login.html', {})

def request(request):
	if request.method == 'POST':
		request_form = RequestForm(request.POST)
		
		if request_form.is_valid():
			request_form.save()
			return redirect('home')
	else:
		request_form = RequestForm()
	return render(request, 'tutor/request.html', {'request_form':request_form})
