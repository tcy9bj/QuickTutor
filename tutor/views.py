from django.shortcuts import render
from django.shortcuts import redirect

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
	form = RequestForm()
	if request.method == 'POST':
		form = RequestForm(request.POST)
		print(form.errors)
		if form.is_valid():
			print("hi")
			form.save()
			fName = form.cleaned_data['fName']
			lName = form.cleaned_data['lName']
			subject = form.cleaned_data['subject']
			question = form.cleaned_data['question']
			form.save()
		else:
			print("hey")
			form = RequestForm()
	return render(request, 'tutor/request.html')
