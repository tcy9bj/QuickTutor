from django.shortcuts import render
from django.shortcuts import redirect

from users.models import Profile
from tutor.forms import RequestForm

def home(request):
	tutors = Profile.objects.filter(active=True)
	context = {'tutors': tutors}
	return render(request, 'tutor/home.html', context)

def login(request):
    return render(request, 'tutor/login.html', {})

def request(request):
	if request.method == 'POST':
		form = RequestForm(request.POST)
		if form.is_valid():
			form.save()
			form = RequestForm()
			return redirect('home', pk=post.pk)
	else:
		form = RequestForm()
	return render(request, 'tutor/request.html', {})
