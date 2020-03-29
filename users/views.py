from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def register(request):
	if (not request.user.profile.initialized):
		if (request.method == 'POST'):
			user_form = UserUpdateForm(request.POST, instance=request.user)
			profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

			if (user_form.is_valid() and profile_form.is_valid()):
				user_form.save()
				profile = profile_form.save(commit=False)
				profile.user = request.user
				profile.initialized = True
				profile.save()
				messages.success(request, f'Account has been created.')
				return redirect('home')
		else:
			user_form = UserUpdateForm()
			profile_form = ProfileUpdateForm()
		return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})
	else:
		return redirect('home')

def profile(request):
    return render(request, 'users/profile.html', {})