from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, FeedbackForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, DeleteView, CreateView
from django.contrib import messages
from django.urls import reverse
from users.models import Profile, Comment
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
	comments = profile.user.reviewee.all()
	return render(request, 'users/profile.html', {'profile':profile, 'comments':comments})


@login_required
def inbox(request):
	incoming_requests = request.user.receiving_user.filter(accepted=False, declined=False)
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

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, "Your request was successfully deleted.")
		return super(AskDeleteView, self).delete(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('inbox')

	def test_func(self):
		ask = self.get_object()
		if (self.request.user == ask.sender):
			return True
		else:
			return False


class AskCompleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Ask
	template_name = 'users/ask_confirm_completion.html'

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, "Your current request has been completed. You may now accept other incoming requests.")
		return super(AskCompleteView, self).delete(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('inbox')

	def test_func(self):
		ask = self.get_object()
		if (self.request.user == ask.receiver and self.request.user.profile.current_client == ask):
			return True
		else:
			return False


@login_required
def accept_ask(request, ask_id):
	ask = get_object_or_404(Ask, pk=ask_id)
	profile = request.user.profile
	if (profile.current_client):
		messages.error(request, 'You may not accept a new request when you already have an active one. Please complete the request of your current client.')
		return redirect('inbox')
	ask.accepted = True
	profile.current_client = ask
	ask.save()
	profile.save()
	messages.success(request, "You have accepted " + ask.sender.profile.first_name + "'s request for tutoring. You can view his contact information under the current client section.")
	return redirect('inbox')


@login_required
def decline_ask(request, ask_id):
	ask = get_object_or_404(Ask, pk=ask_id)
	ask.declined = True
	ask.save()
	messages.info(request, f"You have declined " + ask.sender.profile.first_name + "'s request.")
	return redirect('inbox')


@login_required
def edit_profile(request, profile_id):
	if (request.method == 'POST'):
		user_form = UserUpdateForm(request.POST, instance=request.user)
		profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if (user_form.is_valid() and profile_form.is_valid()):
			user_form.save()
			profile_form.save()
			messages.success(request, f'Your profile has been updated.')
			return redirect('profile_page', profile_id=profile_id)

	else:
		user_form = UserUpdateForm(instance=request.user)
		profile_form = ProfileUpdateForm(instance=request.user.profile)

	return render(request, 'users/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


class CommentCreateView(LoginRequiredMixin, CreateView):
	model = Comment
	form_class = FeedbackForm

	def get_success_url(self):
		reviewee = get_object_or_404(User, pk=self.kwargs['pk'])
		profile = reviewee.profile
		rating = float(self.object.rating)
		if (profile.tutor_score == None):
			profile.tutor_score = rating
			profile.num_ratings += 1
		else:
			profile.num_ratings += 1
			new_tutor_score = profile.tutor_score + ((rating - profile.tutor_score) / profile.num_ratings)
			profile.tutor_score = round(new_tutor_score, 2)
		profile.save()
		messages.success(self.request, "Your review has been submitted.")
		return reverse('profile_page', kwargs={'profile_id': reviewee.profile.id})

	def form_valid(self, form):
		form.instance.reviewer = self.request.user
		form.instance.reviewee = get_object_or_404(User, pk=self.kwargs['pk'])
		return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	template_name = 'users/comment_confirm_delete.html'

	def delete(self, request, *args, **kwargs):
		comment = self.get_object()
		profile = comment.reviewee.profile
		rating = float(comment.rating)
		if (profile.num_ratings == 1):
			profile.tutor_score = None
			profile.num_ratings -= 1
		else:
			new_tutor_score = (profile.tutor_score - (rating / profile.num_ratings)) / (1 - (1 / profile.num_ratings))
			profile.tutor_score = round(new_tutor_score, 2)
			profile.num_ratings -= 1
		profile.save()
		return super(CommentDeleteView, self).delete(request, *args, **kwargs)

	def get_success_url(self):
		messages.success(self.request, "Your review has been deleted.")
		reviewee = get_object_or_404(User, pk=self.kwargs['user_id'])
		return reverse('profile_page', kwargs={'profile_id': reviewee.profile.id})

	def test_func(self):
		comment = self.get_object()
		if (self.request.user == comment.reviewer):
			return True
		else:
			return False