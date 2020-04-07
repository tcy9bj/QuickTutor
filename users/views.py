from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, DeleteView
from django.contrib import messages
from django.urls import reverse
from users.models import Profile
from tutor.models import Ask

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

@login_required
def profile_page(request, profile_id):
	profile = get_object_or_404(Profile, pk=profile_id)
	return render(request, 'users/profile.html', {'profile':profile})

@login_required
def inbox(request):
	incoming_requests = request.user.receiving_user.all()
	outgoing_requests = request.user.sending_user.all()
	context = {
		'incoming_requests':incoming_requests,
		'outgoing_requests':outgoing_requests
	}
	return render(request, 'users/inbox.html', context)

class AskDetailView(LoginRequiredMixin, DetailView):
	model = Ask
	template_name = 'users/ask_detail.html'

class AskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Ask
	template_name = 'users/ask_confirm_delete.html'

	def get_success_url(self):
		return reverse('inbox')

	def test_func(self):
		ask = self.get_object()
		if (self.request.user == ask.sender):
			return True
		else:
			return False