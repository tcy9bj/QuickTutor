from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.models import Profile
from tutor.forms import RequestForm
from tutor.models import Ask

tutor_locations = ['1515 Student Center','Alderman Library','Astronomy Building','Bryan Hall',
				   'Chemistry Building','Clark Hall','Claude Moore Nursing School','Clemons Library',
				   'Cocke Hall','Curry School','Darden Library','Fine Arts Library','Garrett Hall',
				   'Gilmer Hall','Halsey Hall','Health Sciences Library','Kerchof Hall','Law Library',
				   'Maury Hall','McLeod Hall','Mechanical Engineering Bldg','Minor Hall','Monroe Hall',
				   'Music Library','Nau-Gibson Hall','New Cabell Hall','Newcomb Hall','O-Hill Dining Hall',
				   'Olsson Hall','Physics Bldg','Randall Hall','Rice Hall','Rouss Robertson Hall',
				   'Runk Dining Hall','Special Collections Library','The Castle','The Rotunda',
				   'Thornton Hall','West Range Cafe','Wilsdorf Hall','Wilson Hall',
				   'Other (Central Grounds)', 'Other (E-School)','Other (Med School)',
				   'Other (North Grounds)','Other (The Corner)','Other']

def login(request):
    return render(request, 'tutor/login.html', {})

@login_required
def home(request):
	tutors = Profile.objects.filter(active=True)
	context = {'tutors':tutors, 'locations':tutor_locations}
	return render(request, 'tutor/home.html', context)

@login_required
def activate(request, profile_id):
	selected_location = request.POST.get('location_selector')
	if (not selected_location):
		tutors = Profile.objects.filter(active=True)
		context = {'tutors':tutors, 'locations':tutor_locations, 'error_message':"Please select a location."}
		return render(request, 'tutor/home.html', context)
	else:
		profile = get_object_or_404(Profile, pk=profile_id)
		profile.location = selected_location
		profile.active = True
		profile.save()
	return redirect('home')

@login_required
def deactivate(request, profile_id):
	tutors = Profile.objects.filter(active=True)
	profile = get_object_or_404(Profile, pk=profile_id)
	profile.location = ''
	profile.active = False
	context = {'tutors':tutors, 'locations':tutor_locations}
	profile.save()
	return redirect('home')

def request(request):
	if request.method == 'POST':
		request_form = RequestForm(request.POST)
		
		if request_form.is_valid():
			request_form.save()
			return redirect('home')
	else:
		request_form = RequestForm()
	return render(request, 'tutor/request.html', {'request_form':request_form})
